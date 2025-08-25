# Command Help
## Command Updating
```Used to update commands on the backend.```
### Arguments
- [>0] **update**: Reloads '/assets/discord_bot/commands.json'
## Command Modifications Help Page
```Used to create and modify commands. Arguments with '>' are required... Arguments with '~' are optional```
### Arguments
- [>0] **-m**: Enables modify mode
- [>1] **\<name\>**: Command name
- [~2] **\<target\>**: Command aspect to be modified. Options include... **-d [dir] | -f [file (default)]**
- [~3] **\<source\>**: Command type to be modified. Options include... **-j [json (default)] | -m [manual] | -s [script]**
- [~4] **\<modify-mode\>**: Method of modification. Options include... **~~-c [create]~~ | -v [view (default)] | ~~-e [edit]~~ | ~~-r [replace]~~ | ~~-d [destroy]~~**
