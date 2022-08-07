import boilerBot as bb


botClient = bb.bot(bb.lib.cfg['options']['prefix'], defaultGuildVars={"player":None,"previous":None},intents=bb.intents)
bb.atexit.register(botClient.shutdown)
botClient.run(bb.lib.cfg['discord']['token'])