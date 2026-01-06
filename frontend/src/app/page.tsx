"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { healthApi } from "@/lib/api";

export default function Home() {
  const { data: health, isLoading } = useQuery({
    queryKey: ["health"],
    queryFn: healthApi.check,
  });

  return (
    <div className="flex min-h-screen flex-col">
      {/* Hero Section */}
      <section className="flex flex-1 items-center justify-center bg-gradient-to-b from-zinc-50 to-white px-4 py-20">
        <div className="container max-w-6xl">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-zinc-900 sm:text-6xl">
              LoteriaTech
            </h1>
            <p className="mt-6 text-lg leading-8 text-zinc-600">
              Análise espacial e estatística de loterias brasileiras
            </p>
            <div className="mt-10 flex items-center justify-center gap-4">
              <Button asChild size="lg">
                <Link href="/lotteries">Ver Loterias</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/auth/login">Entrar</Link>
              </Button>
            </div>
          </div>

          {/* Status Cards */}
          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Status da API</CardTitle>
                <CardDescription>Conexão com backend</CardDescription>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <p className="text-sm text-zinc-500">Verificando...</p>
                ) : health ? (
                  <div className="space-y-1">
                    <p className="text-sm">
                      <span className="font-medium">Status:</span>{" "}
                      <span className="text-green-600">✓ {health.status}</span>
                    </p>
                    <p className="text-sm">
                      <span className="font-medium">Ambiente:</span> {health.environment}
                    </p>
                    <p className="text-sm">
                      <span className="font-medium">Database:</span> {health.database}
                    </p>
                  </div>
                ) : (
                  <p className="text-sm text-red-600">✗ Backend offline</p>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Mega-Sena</CardTitle>
                <CardDescription>Análise espacial 10×6</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-zinc-600">
                  60 números organizados em grade 10×6 com 27 features espaciais calculadas.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Lotofácil</CardTitle>
                <CardDescription>Análise espacial 5×5</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-zinc-600">
                  25 números organizados em grade 5×5 com análise de frequência e padrões.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-6">
        <div className="container text-center text-sm text-zinc-600">
          <p>LoteriaTech v1.0.0 - Plataforma de análise de loterias</p>
        </div>
      </footer>
    </div>
  );
}
