import os
import uuid
from typing import Any, Optional

from app.core.logging import get_logger

logger = get_logger(__name__)

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")

_graph_data_cache: dict = {}


def _node_id(prefix: str, key: str) -> str:
    return f"{prefix}:{key}"


class KnowledgeGraph:
    def __init__(self) -> None:
        self._driver: Any = None
        self._enabled = False
        self._init()

    def _init(self) -> None:
        try:
            from neo4j import AsyncGraphDatabase
            self._driver = AsyncGraphDatabase.driver(NEO4J_URI)
            self._enabled = True
            logger.info("KnowledgeGraph connected to %s", NEO4J_URI)
        except Exception as exc:
            logger.warning("KnowledgeGraph disabled (neo4j not available): %s", exc)
            self._enabled = False

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()

    async def clear(self) -> None:
        if not self._enabled:
            return
        try:
            async with self._driver.session(database="neo4j") as session:
                await session.run("MATCH (n) DETACH DELETE n")
            _graph_data_cache.clear()
        except Exception as exc:
            logger.error("KnowledgeGraph clear failed: %s", exc)

    async def upsert_target(self, target_id: str, name: str, scan_id: str, scan_type: str = "") -> None:
        if not self._enabled:
            return
        try:
            async with self._driver.session(database="neo4j") as session:
                await session.run(
                    """
                    MERGE (t:Target {id: $id})
                    SET t.name = $name, t.scan_id = $scan_id,
                        t.scan_type = $scan_type, t.last_seen = timestamp()
                    """,
                    id=target_id, name=name, scan_id=scan_id, scan_type=scan_type,
                )
        except Exception as exc:
            logger.error("KnowledgeGraph upsert_target failed: %s", exc)

    async def upsert_port(self, target_id: str, port: int, protocol: str, state: str) -> str:
        if not self._enabled:
            return _node_id("port", f"{target_id}:{port}")
        pid = _node_id("port", f"{target_id}:{port}")
        try:
            async with self._driver.session(database="neo4j") as session:
                await session.run(
                    """
                    MERGE (p:Port {id: $pid})
                    SET p.port = $port, p.protocol = $protocol,
                        p.state = $state, p.last_seen = timestamp()
                    """,
                    pid=pid, port=port, protocol=protocol, state=state,
                )
                await session.run(
                    """
                    MATCH (t:Target {id: $target_id})
                    MATCH (p:Port {id: $pid})
                    MERGE (t)-[r:HAS_PORT]->(p)
                    SET r.last_seen = timestamp()
                    """,
                    target_id=target_id, pid=pid,
                )
        except Exception as exc:
            logger.error("KnowledgeGraph upsert_port failed: %s", exc)
        return pid

    async def upsert_service(self, port_id: str, name: str, version: str = "", banner: str = "") -> str:
        if not self._enabled:
            return _node_id("service", f"{port_id}:{name}")
        sid = _node_id("service", f"{port_id}:{name}")
        try:
            async with self._driver.session(database="neo4j") as session:
                await session.run(
                    """
                    MERGE (s:Service {id: $sid})
                    SET s.name = $name, s.version = $version,
                        s.banner = $banner, s.last_seen = timestamp()
                    """,
                    sid=sid, name=name, version=version, banner=banner,
                )
                await session.run(
                    """
                    MATCH (p:Port {id: $port_id})
                    MATCH (s:Service {id: $sid})
                    MERGE (p)-[r:RUNS]->(s)
                    SET r.last_seen = timestamp()
                    """,
                    port_id=port_id, sid=sid,
                )
        except Exception as exc:
            logger.error("KnowledgeGraph upsert_service failed: %s", exc)
        return sid

    async def add_finding(
        self,
        target_id: str,
        title: str,
        severity: str,
        description: str = "",
        remediation: str = "",
        tool_name: str = "",
        port_id: str = "",
        service_id: str = "",
    ) -> str:
        if not self._enabled:
            return _node_id("finding", str(uuid.uuid4().hex[:8]))
        fid = _node_id("finding", str(uuid.uuid4().hex[:8]))
        try:
            async with self._driver.session(database="neo4j") as session:
                await session.run(
                    """
                    MERGE (f:Finding {id: $fid})
                    SET f.title = $title, f.severity = $severity,
                        f.description = $description, f.remediation = $remediation,
                        f.tool = $tool_name, f.created_at = timestamp()
                    """,
                    fid=fid, title=title, severity=severity,
                    description=description, remediation=remediation,
                    tool_name=tool_name,
                )
                await session.run(
                    """
                    MATCH (t:Target {id: $target_id})
                    MATCH (f:Finding {id: $fid})
                    MERGE (t)-[r:HAS_FINDING]->(f)
                    """,
                    target_id=target_id, fid=fid,
                )
                if tool_name:
                    tid = _node_id("tool", tool_name)
                    await session.run(
                        """
                        MERGE (t:Tool {id: $tid})
                        SET t.name = $tool_name
                        """,
                        tid=tid, tool_name=tool_name,
                    )
                    await session.run(
                        """
                        MATCH (f:Finding {id: $fid})
                        MATCH (t:Tool {id: $tid})
                        MERGE (f)-[r:DETECTED_BY]->(t)
                        """,
                        fid=fid, tid=tid,
                    )
                if port_id:
                    await session.run(
                        """
                        MATCH (f:Finding {id: $fid})
                        MATCH (p:Port {id: $port_id})
                        MERGE (f)-[r:EXPLOITS]->(p)
                        """,
                        fid=fid, port_id=port_id,
                    )
                if service_id:
                    await session.run(
                        """
                        MATCH (f:Finding {id: $fid})
                        MERGE (s:Service {id: $service_id})
                        MERGE (f)-[r:AFFECTS]->(s)
                        """,
                        fid=fid, service_id=service_id,
                    )
        except Exception as exc:
            logger.error("KnowledgeGraph add_finding failed: %s", exc)
        return fid

    async def fetch_graph(self, scan_id: str = "") -> dict:
        if not self._enabled:
            return {"nodes": [], "edges": []}
        try:
            async with self._driver.session(database="neo4j") as session:
                if scan_id:
                    result = await session.run(
                        """
                        MATCH (n)-[r]->(m)
                        WHERE n.scan_id = $scan_id OR m.scan_id = $scan_id
                        RETURN n, r, m
                        """,
                        scan_id=scan_id,
                    )
                else:
                    result = await session.run(
                        "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 500"
                    )

                nodes_map: dict[str, dict] = {}
                edges: list[dict] = []
                edge_set: set[str] = set()

                async for record in result:
                    for node_key in ("n", "m"):
                        node = record.get(node_key)
                        if node and node.element_id not in nodes_map:
                            props = dict(node)
                            label = list(node.labels)[0] if node.labels else "Node"
                            nodes_map[node.element_id] = {
                                "id": props.get("id", node.element_id),
                                "label": props.get("name") or props.get("title") or label,
                                "group": label.lower(),
                                "title": _node_tooltip(props, label),
                                "severity": props.get("severity", ""),
                                "port": props.get("port"),
                            }

                    rel = record.get("r")
                    if rel:
                        rel_type = rel.type
                        rid = f"{rel.start_node.element_id}-{rel_type}->{rel.end_node.element_id}"
                        if rid not in edge_set:
                            edge_set.add(rid)
                            start_node = record["n"]
                            end_node = record["m"]
                            edges.append({
                                "from": dict(start_node).get("id", start_node.element_id),
                                "to": dict(end_node).get("id", end_node.element_id),
                                "label": rel_type,
                                "arrows": "to",
                            })

                return {"nodes": list(nodes_map.values()), "edges": edges}
        except Exception as exc:
            logger.error("KnowledgeGraph fetch_graph failed: %s", exc)
            return {"nodes": [], "edges": []}


def _node_tooltip(props: dict, label: str) -> str:
    lines = [f"<b>{label}</b>"]
    for k, v in props.items():
        if k not in ("id",) and v:
            lines.append(f"{k}: {v}")
    return "<br>".join(lines[:8])


_graph: Optional[KnowledgeGraph] = None


def get_knowledge_graph() -> KnowledgeGraph:
    global _graph
    if _graph is None:
        _graph = KnowledgeGraph()
    return _graph
