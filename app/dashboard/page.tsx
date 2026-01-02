import { MotionConfig, motion } from "framer-motion";
import { Activity, Brain, TrendingUp, Users, MessageCircle, Zap } from "lucide-react";

export default function Dashboard() {
  return (
    <MotionConfig transition={{ duration: 0.6, ease: "easeOut" }}>
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white" dir="rtl">
        {/* Hero */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="container mx-auto px-6 pt-20 pb-10 text-center"
        >
          <h1 className="text-6xl font-black mb-6 bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-violet-500">
            تحلیلگر هوشمند شبکه‌های اجتماعی پارسی
          </h1>
          <p className="text-2xl text-purple-200 mb-8 font-light">
            اولین پلتفرم هوش مصنوعی تخصصی برای تحلیل محتوای پارسی
          </p>
          <div className="flex justify-center gap-8 text-5xl">
            <Zap className="text-yellow-400 animate-pulse" />
            <Brain className="text-cyan-400" />
            <TrendingUp className="text-green-400" />
          </div>
        </motion.div>

        {/* Live Stats */}
        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="grid grid-cols-2 md:grid-cols-4 gap-6 container mx-auto px-6 max-w-6xl"
        >
          {[
            { icon: Activity, label: "پست‌های تحلیل شده", value: "۴۸,۷۲۹", color: "from-pink-500 to-rose-500" },
            { icon: Users, label: "نویسندگان فعال", value: "۱۲,۴۸۳", color: "from-cyan-500 to-blue-500" },
            { icon: MessageCircle, label: "ترندهای امروز", value: "۴۷", color: "from-green-500 to-emerald-500" },
            { icon: Brain, label: "دقت احساسات", value: "۹۲.۳٪", color: "from-purple-500 to-violet-500" },
          ].map((stat, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.05 }}
              className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 border border-white/20 shadow-2xl"
            >
              <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${stat.color} p-4 mb-4`}>
                <stat.icon className="w-full h-full" />
              </div>
              <p className="text-4xl font-black mb-2">{stat.value}</p>
              <p className="text-purple-200">{stat.label}</p>
            </motion.div>
          ))}
        </motion.div>

        <div className="text-center mt-20 pb-20">
          <motion.button
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            className="bg-gradient-to-r from-pink-500 to-violet-500 text-white text-2xl font-bold px-16 py-8 rounded-full shadow-2xl"
          >
            شروع تحلیل زنده
          </motion.button>
        </div>
      </div>
    </MotionConfig>
  );
}
