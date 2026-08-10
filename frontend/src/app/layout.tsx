import type { Metadata } from "next";
import localFont from "next/font/local";
import "../styles/globals.css";
import "reactflow/dist/style.css";

const inter = localFont({
  src: "./fonts/inter-var.ttf",
  variable: "--font-inter",
  weight: "100 900",
  display: "swap",
});

export const metadata: Metadata = {
  title: "AstraIX Security Analyst",
  description: "AI-Powered Autonomous Security Assessment Platform",
  keywords: ["security", "vulnerability", "assessment", "AI", "cybersecurity"],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}