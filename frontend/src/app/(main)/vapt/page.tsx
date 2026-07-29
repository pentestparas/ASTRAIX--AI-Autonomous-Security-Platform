"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function VaptPage() {
  const router = useRouter();
  useEffect(() => { router.replace("/scans"); }, [router]);
  return null;
}