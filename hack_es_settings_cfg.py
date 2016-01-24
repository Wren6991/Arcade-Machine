# Can't use XML library because es_systems.cfg isn't always well-formed
import re

# Fuck it, use regular expressions


def amend_system(matchobj):
    system_name = re.search("<name>([^<]*?)</name>", matchobj.group(0)).group(1)
    sys_string = matchobj.group(0)
    old_command = re.search("<command>([\d\D]*?)</command>", sys_string).group(1)
    return re.sub("<command>([\d\D]*?)</command>",
     "<command>sudo python /home/pi/on_game_start.py " + system_name + ' "%ROM%" && ' + old_command + ' && sudo python /home/pi/on_game_exit.py</command>',
    sys_string)

	
cfgdata = open("/etc/emulationstation/es_systems.cfg").read()

cfgdata = re.sub("<system>[\d\D]*?</system>", amend_system, cfgdata)

of = open("hacked_es_systems.cfg", "w")
of.write(cfgdata)
of.close()

