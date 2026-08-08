#
# Description:	initializes one second function for triggers
# Called by:	#minecraft:load
# Entity @s:	None
#
schedule function wyrd_painting:second 1s
#
# scoreboard triggered
#
execute as @a[scores={painting=1..}] at @s run function wyrd_painting:trigger
#
# enables scoreboard
#
scoreboard players set @a[scores={painting=1..}] painting 0
scoreboard players enable @a painting