#!/usr/bin/env python3
"""
🛡️ Pi Telegram Gateway
Control Pi-Swarm Security Edition from Telegram
Same as OpenClaw's channel integration
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add pi_core to path
sys.path.insert(0, str(Path(__file__).parent))

from pi_core.provider import PiClawProvider

# Telegram Bot Configuration
# User should set this: export PI_TELEGRAM_TOKEN="your_bot_token"
TELEGRAM_TOKEN = os.getenv("PI_TELEGRAM_TOKEN", "")

class TelegramGateway:
    """Pi-Swarm control via Telegram - OpenClaw style channel integration"""
    
    def __init__(self):
        self.ai = PiClawProvider()
        self.allowed_users = []  # Add authorized Telegram user IDs here
        
    async def run(self):
        """Run the Telegram bot"""
        if not TELEGRAM_TOKEN:
            print("❌ Set PI_TELEGRAM_TOKEN environment variable")
            print("   export PI_TELEGRAM_TOKEN='your_bot_token'")
            return
            
        try:
            from telegram import Update
            from telegram.ext import Application, CommandHandler, MessageHandler, filters
        except ImportError:
            print("❌ Install python-telegram-bot: pip install python-telegram-bot")
            return
        
        app = Application.builder().token(TELEGRAM_TOKEN).build()
        
        # Command handlers (OpenClaw style)
        app.add_handler(CommandHandler("start", self.cmd_start))
        app.add_handler(CommandHandler("status", self.cmd_status))
        app.add_handler(CommandHandler("audit", self.cmd_audit))
        app.add_handler(CommandHandler("scan", self.cmd_scan))
        app.add_handler(CommandHandler("task", self.cmd_task))
        app.add_handler(CommandHandler("agent", self.cmd_agent))
        app.add_handler(CommandHandler("help", self.cmd_help))
        
        # Message handler
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        print("🛡️ Pi Telegram Gateway Started")
        print("   Send /start to your bot")
        
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        
        # Keep running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await app.stop()
    
    async def cmd_start(self, update: Update, context):
        """Welcome message"""
        await update.message.reply_text(
            "🛡️ Pi-Swarm Security Edition\n"
            "Enhanced OpenClaw with Security Tools\n\n"
            "Commands:\n"
            "/status - Check system\n"
            "/audit \u003ctarget\u003e - Security audit\n"
            "/scan \u003cip\u003e - Network scan\n"
            "/task \u003cdesc\u003e - Autonomous task\n"
            "/agent \u003cmsg\u003e - Chat with AI\n"
            "/help - Show help"
        )
    
    async def cmd_status(self, update: Update, context):
        """System status"""
        try:
            # Check Ollama
            import urllib.request
            req = urllib.request.Request(
                "http://localhost:11434/api/generate",
                data=json.dumps({"model": "qwen2.5:1.5b", "prompt": "status", "stream": False}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5):
                status = "🟢 Online"
        except:
            status = "🔴 Offline"
        
        await update.message.reply_text(
            f"🛡️ Pi-Swarm Status\n"
            f"AI Core: {status}\n"
            f"Security Tools: 🟢 Loaded\n"
            f"Mode: OpenClaw-Enhanced"
        )
    
    async def cmd_audit(self, update: Update, context):
        """Security audit command"""
        if not context.args:
            await update.message.reply_text("Usage: /audit \u003cfile_or_url\u003e")
            return
        
        target = context.args[0]
        await update.message.reply_text(f"🔍 Auditing: {target}...")
        
        # Run the security agent
        from pi_core.agent_runner import AgentRunner
        agent = AgentRunner(f"audit {target}")
        result = agent.run()
        
        # Truncate if too long for Telegram
        if len(result) > 4000:
            result = result[:4000] + "\n\n[...truncated]"
        
        await update.message.reply_text(result)
    
    async def cmd_scan(self, update: Update, context):
        """Network scan command"""
        if not context.args:
            await update.message.reply_text("Usage: /scan \u003cip_or_range\u003e")
            return
        
        target = context.args[0]
        await update.message.reply_text(f"📡 Scanning {target}...")
        
        from pi_core.agent_runner import AgentRunner
        agent = AgentRunner(f"scan {target}")
        result = agent.run()
        
        await update.message.reply_text(result[:4000])
    
    async def cmd_task(self, update: Update, context):
        """Autonomous task command"""
        if not context.args:
            await update.message.reply_text("Usage: /task \u003csecurity_task_description\u003e")
            return
        
        task = " ".join(context.args)
        await update.message.reply_text(f"🚀 Task: {task}\nExecuting...")
        
        from pi_core.agent_runner import AgentRunner
        agent = AgentRunner(task)
        result = agent.run()
        
        await update.message.reply_text(result[:4000])
    
    async def cmd_agent(self, update: Update, context):
        """Direct AI conversation"""
        if not context.args:
            await update.message.reply_text("Usage: /agent \u003cmessage\u003e")
            return
        
        message = " ".join(context.args)
        
        # Direct AI chat
        response = self.ai.ask_ai(
            message,
            "You are Pi-Swarm Security Agent. Help with security questions."
        )
        
        await update.message.reply_text(response[:4000])
    
    async def cmd_help(self, update: Update, context):
        """Help command"""
        help_text = """🛡️ Pi-Swarm Security Edition

Commands:
/status - Check system status
/audit \u003ctarget\u003e - Security audit (file or URL)
/scan \u003cip\u003e - Network scan
/task \u003cdesc\u003e - Autonomous security task
/agent \u003cmsg\u003e - Direct AI chat
/help - Show this help

Examples:
/audit https://github.com/user/repo
/scan 192.168.1.1
/task Find vulnerabilities in .sol files
/agent What is reentrancy attack?
"""
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context):
        """Handle plain text messages"""
        text = update.message.text
        
        # Treat as direct agent query
        response = self.ai.ask_ai(
            text,
            "You are Pi-Swarm Security Agent."
        )
        
        await update.message.reply_text(response[:4000])

def main():
    """CLI entry"""
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        print("🛡️ Pi Telegram Setup")
        print("1. Create bot with @BotFather on Telegram")
        print("2. Get your token")
        print("3. Run: export PI_TELEGRAM_TOKEN='your_token'")
        print("4. Run: python3 pi_telegram.py")
        return
    
    gateway = TelegramGateway()
    asyncio.run(gateway.run())

if __name__ == "__main__":
    main()
