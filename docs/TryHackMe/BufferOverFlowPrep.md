# BufferOverFlowPrep

This room is a nice practice zone for buffer overflow exploit development. I've already completed the first two tasks which include launching the VM and a buffer overflow leveraging `mona` in immunity debugger to increase speed.

I see a lot of automation potential in the exploit provided in task 2. So I will use this series to come up with a toolset to automate this crap so I never have to do it again.

Initially I was going to document my journey as I developed the tool, but it was too much extra work. [Here's the code](https://github.com/nlw93/oscpTools/blob/main/bof.ps1). Only runs on linux and `xclip` required. It could easily be ported to Windows, just need to change the functions that access clipboard. 

LMK if you have any questions!

