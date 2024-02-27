import frida
from customtkinter import *

from MainWindow import MainWindow

session: frida.core.Session
fun = 0x0

mainWindow = None # type: MainWindow

def scan(pattern):
    # code from poxyran/misc
    script = session.create_script("""
        var ranges = Process.enumerateRangesSync({protection: 'r--', coalesce: true});
        var range;

        function processNext(){
            var match = false;

            range = ranges.pop();
            if (!range) {
                return;
            }

            Memory.scan(range.base, range.size, '%s', {
                onMatch: function(address, size) {
                    send(address.toString());
                    match = true;
                    return "stop";
                },
                onError: function(reason){
                    console.log('[!] There was an error scanning memory');
                },
                onComplete: function(){
                    if (match == true) { return; }
                    processNext();
                }
            });
        }

        processNext();
    """ % pattern)

    script.on('message', on_scan_msg)
    script.load()


def on_scan_msg(message, data):
    global fun
    fun = int(message["payload"], 16) + 0x7     # arbitrary offset
    # print("Pattern matched at address %s" % hex(fun))
    read(fun)


def read(address):
    script = session.create_script("""
        Interceptor.attach(ptr("0x%x"), {
            onEnter(args) {
                var x = this.context;
                send(x);
            }
        });
    """ % address)

    script.on('message', on_read_msg)
    script.load()


def on_read_msg(message, data):
    rax = int(message["payload"]["rax"], 16)
    if rax == 0:
        return

    rsi = message["payload"]["rsi"]

    global mainWindow

    if rax >= 9999999:
        if mainWindow.last_timer_mem != rsi and mainWindow.last_timer_mem != 1: # Reach end of quest, save run
            mainWindow.last_timer_mem = rsi
            mainWindow.save_run()
        else:
            mainWindow.update(mainWindow.getTimeElapsed() + 1, mainWindow.getParseTotal())
    else:
        mainWindow.update(mainWindow.getTimeElapsed() ,mainWindow.getParseTotal() + rax)


def main():
    global session
    global mainWindow
    try:
        session = frida.attach("granblue_fantasy_relink.exe")
    except frida.ProcessNotFoundError:
        mainWindow = MainWindow(True)
        return

    scan("FF 50 78 8B 44 24 40 89 87 D0 00 00 00 45 85 E4 74 6C")       # damage
    scan("BE AC 02 00 00 74 71 89 BE AC 02 00 00 8D 47 FF")             # timer
    mainWindow = MainWindow()


if __name__ == '__main__':
    main()
    if mainWindow:
        mainWindow.mainLoop()

