from src.app.application import App
import getopt, sys

APPLICATION_NAME = "Evourge"


def processCommand(app, args):

    commandContext = {"Help": "This is the help text", \
                        "Display": "Set display size (Example: 800,600)", \
                        "PygameOptions": "Set PYGAME surface options (Example: pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)", \
                        "ColorDepth": "Set the color depth for the display", \
                        "ScreenID": "ID number of display to use", \
                        "Vsync": "Enable VSYNV (BOOL 0 or 1, Default: 1)", \
                        "Mute": "Mute or Unmute sounds (BOOL 0 or 1, Default: 1)", \
                        "FPS": "Set the graphics engin FPS (Default: 30)"}

    description = f'Application {APPLICATION_NAME}'

    # Long options
    long_options = commandContext.keys()

    short = []
    setShort = set()
    for option in long_options:
        short.append(option[0].lower())
        setShort.add(short[-1])

    try:
        if len(short) != len(setShort):
            raise Exception("Short Command Conflict!")
        options = "".join(short) + ":"
    except Exception as error:
        print('Caught this error: ' + repr(error))


    try:
        # Parsing argument
        arguments, values = getopt.getopt(args[1:], options, long_options)
        
        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--Help"):
                print(f'{args[0]} help...')
                print(f'{description}')
                print(f'\n\nCommands:')

                for command, help in commandContext.items():
                    print(f'   --{command} {help}')

                print('\n')

                return False
            
            elif currentArgument in ("-d", "--Display"):
                app.gui.window.width, app.gui.window.height = currentValue.split(",")
            elif currentArgument in ("-p", "--PygameOptions"):
                app.gui.setSurfaceOptions(currentValue)
            elif currentArgument in ("-c", "--ColorDepth"):
                app.gui.colorDepth = currentValue
            elif currentArgument in ("-s", "--ScreenID"):
                app.gui.screenID = currentValue
            elif currentArgument in ("-v", "--Vsync"):
                app.gui.vsync = currentValue
            elif currentArgument in ("-f", "--FPS"):
                app.gui.fps = currentValue
        return True
                
    except getopt.error as err:
        # output error, and return with an error code
        print (str(err))
        return False


if __name__ == "__main__":
    #Program Entry

    myApp = App()

    if processCommand(myApp, sys.argv):
        myApp.run()

