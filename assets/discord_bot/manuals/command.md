# Edit Command Help
## Updating Commands
```Reloads all commands in the bot.```
### Arguments
- r.[0] **update**: Reloads '/assets/discord_bot/commands.json'
## Modify Commands
```Used to create and modify commands. Arguments with '>' are required... Arguments with '~' are optional```
### Arguments
- r.[0] **-m**: Enables modify mode
- r.[1] **\<name\>**: Command name
- o.[2] **\<target\>**: Command aspect to be modified. Options include... **-d [dir] | -f [file (default)]**
- o.[3] **\<source\>**: Command type to be modified. Options include... **-j [json (default)] | -m [manual] | -s [script]**
- o.[4] **\<modify-mode\>**: Method of modification. Options include... **~~-c [create]~~ | -v [view (default)] | ~~-e [edit]~~ | ~~-r [replace]~~ | ~~-d [destroy]~~**
