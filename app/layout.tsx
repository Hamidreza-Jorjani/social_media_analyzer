import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "تحلیلگر هوشمند پارسی",
  description: "اولین پلتفرم تحلیل محتوای پارسی با هوش مصنوعی",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fa" dir="rtl">
      <body className="antialiased">{children}</body>
    </html>
  );
}
