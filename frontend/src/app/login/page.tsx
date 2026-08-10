"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authApi, organizationsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Radar, Loader2 } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fullName, setFullName] = useState("");
  const [orgName, setOrgName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await authApi.login(email, password);
      const tokenData = res as unknown as { access_token?: string; token_type?: string; expires_in?: number };
      if (tokenData.access_token) {
        localStorage.setItem("access_token", tokenData.access_token);
        const userRes = await authApi.me();
        const userData = userRes as unknown as { id?: string; email?: string; organization_id?: string };
        if (userData.id) {
          localStorage.setItem("user_id", userData.id);
          localStorage.setItem("user_email", userData.email || email);
          if (userData.organization_id) {
            localStorage.setItem("organization_id", userData.organization_id);
          }
        }
        // If no organization_id from user, try to get it from organizations list
        const orgId = localStorage.getItem("organization_id");
        if (!orgId) {
          const orgsRes = await organizationsApi.list();
          // Backend returns array directly
          const orgs = (orgsRes as unknown as Array<{ id?: string }>) || [];
          if (orgs.length > 0 && orgs[0].id) {
            localStorage.setItem("organization_id", orgs[0].id);
          }
        }
        router.push("/dashboard");
      } else {
        setError("Login failed - no token received");
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  }

  async function handleRegister(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await authApi.register({
        email,
        password,
        full_name: fullName,
        organization_name: orgName,
        organization_slug: orgName.toLowerCase().replace(/\s+/g, "-"),
      });
      if (res) {
        const loginRes = await authApi.login(email, password);
        const tokenData = loginRes as unknown as { access_token?: string };
        if (tokenData.access_token) {
          localStorage.setItem("access_token", tokenData.access_token);
          // Get organizations - backend returns array directly
          const orgsRes = await organizationsApi.list();
          const orgs = (orgsRes as unknown as Array<{ id?: string }>) || [];
          if (orgs.length > 0 && orgs[0].id) {
            localStorage.setItem("organization_id", orgs[0].id);
          }
          router.push("/dashboard");
        }
      } else {
        setError("Registration failed");
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Registration failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex bg-background">
      <div className="relative hidden lg:flex w-1/2 items-center justify-center overflow-hidden border-r border-border/70 bg-grid">
        <div
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(ellipse 60% 50% at 30% 20%, hsl(188 94% 47% / 0.14), transparent 60%), radial-gradient(ellipse 50% 40% at 75% 80%, hsl(262 83% 63% / 0.12), transparent 60%)",
          }}
        />
        <div className="relative z-10 max-w-md text-center px-8">
          <div className="flex items-center justify-center gap-3 mb-6">
            <div className="relative flex items-center justify-center w-14 h-14 rounded-2xl btn-gradient glow-primary shadow-lg">
              <Radar className="w-8 h-8 text-primary-foreground" />
            </div>
            <div className="text-left leading-tight">
              <span className="block text-3xl font-bold tracking-tight">
                Astra<span className="text-gradient">IX</span>
              </span>
              <span className="block text-xs uppercase tracking-[0.2em] text-muted-foreground">
                Security Analyst
              </span>
            </div>
          </div>
          <h1 className="text-3xl font-bold tracking-tight mb-3">
            Autonomous AI Security{" "}
            <span className="text-gradient">Operations</span>
          </h1>
          <p className="text-muted-foreground leading-relaxed">
            Real Kali container scanning · multi-agent vulnerability
            analysis · AI executive reports · attack surface graphs
          </p>
          <div className="mt-8 grid grid-cols-3 gap-3">
            {[
              { label: "18+ tools", value: "Kali fleet" },
              { label: "3 agents", value: "recon · research · verify" },
              { label: "3 formats", value: "HTML · PDF · JSON" },
            ].map((f) => (
              <div key={f.label} className="rounded-xl border border-border/70 bg-card/50 p-3">
                <p className="text-[10px] uppercase tracking-wider text-muted-foreground">{f.label}</p>
                <p className="text-sm font-semibold mt-1">{f.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-md space-y-6 animate-slide-up">
          <div className="text-center lg:hidden">
            <div className="flex items-center justify-center gap-2 mb-4">
              <div className="relative flex items-center justify-center w-10 h-10 rounded-xl btn-gradient glow-primary">
                <Radar className="w-5 h-5 text-primary-foreground" />
              </div>
              <div className="leading-tight text-left">
                <span className="block text-xl font-bold tracking-tight">Astra<span className="text-gradient">IX</span></span>
                <span className="block text-[10px] uppercase tracking-[0.16em] text-muted-foreground">Security Analyst</span>
              </div>
            </div>
          </div>
          <div className="hidden lg:block">
            <p className="eyebrow mb-2">Workspace</p>
            <h2 className="text-2xl font-bold tracking-tight">{isLogin ? "Sign in" : "Create your workspace"}</h2>
          </div>

        <Card className="glass-card-hover">
          <CardContent className="p-6">
            <div className="lg:hidden mb-4">
              <p className="text-lg font-bold">{isLogin ? "Sign in" : "Create your workspace"}</p>
            </div>
            <form onSubmit={isLogin ? handleLogin : handleRegister} className="space-y-4">
              {!isLogin && (
                <>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Full Name</label>
                    <Input
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="John Doe"
                      required
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-2 block">Organization Name</label>
                    <Input
                      value={orgName}
                      onChange={(e) => setOrgName(e.target.value)}
                      placeholder="Acme Security"
                      required
                    />
                  </div>
                </>
              )}
              <div>
                <label className="text-sm font-medium mb-2 block">Email</label>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  required
                  autoComplete="email"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">Password</label>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  minLength={8}
                  autoComplete="current-password"
                />
              </div>

              {error && (
                <p className="text-sm text-destructive bg-destructive/10 px-3 py-2 rounded-lg">
                  {error}
                </p>
              )}

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : null}
                {isLogin ? "Sign In" : "Create Account"}
              </Button>
            </form>

            <div className="mt-4 text-center text-sm text-muted-foreground">
              {isLogin ? (
                <>
                  Don&apos;t have an account?{" "}
                  <button
                    onClick={() => { setIsLogin(false); setError(""); }}
                    className="text-primary hover:underline hover:text-primary/80"
                  >
                    Sign up
                  </button>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <button
                    onClick={() => { setIsLogin(true); setError(""); }}
                    className="text-primary hover:underline hover:text-primary/80"
                  >
                    Sign in
                  </button>
                </>
              )}
            </div>
          </CardContent>
        </Card>
        </div>
      </div>
    </div>
  );
}