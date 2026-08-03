"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { authApi, organizationsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, Loader2 } from "lucide-react";

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
    <div className="min-h-screen flex items-center justify-center bg-background p-4">
      <div className="w-full max-w-md space-y-6">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Activity className="w-8 h-8 text-primary" />
            <span className="text-2xl font-bold">AstraIX</span>
          </div>
          <p className="text-muted-foreground">
            AI-Powered Security Assessment Platform
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>{isLogin ? "Sign In" : "Create Account"}</CardTitle>
          </CardHeader>
          <CardContent>
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

            <div className="mt-4 text-center text-sm">
              {isLogin ? (
                <>
                  Don&apos;t have an account?{" "}
                  <button
                    onClick={() => { setIsLogin(false); setError(""); }}
                    className="text-primary hover:underline"
                  >
                    Sign up
                  </button>
                </>
              ) : (
                <>
                  Already have an account?{" "}
                  <button
                    onClick={() => { setIsLogin(true); setError(""); }}
                    className="text-primary hover:underline"
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
  );
}