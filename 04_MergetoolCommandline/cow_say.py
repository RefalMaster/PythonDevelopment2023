import cmd
import shlex
from cowsay import cowsay, cowthink, make_bubble, list_cows

class CommandLine(cmd.Cmd):
    def _get_parsed_with_default(self, args, default=""):
        parsed = shlex.split(args)
        if len(parsed) == 0:
            parsed = [default]
        return parsed

    def _get_cowsay_params(self, args):
        parsed = self._get_parsed_with_default(args)
        params = {
            'message': parsed[0],
            'cow': 'default',
            'eyes': 'oo',
            'tongue': '  '
        }
        for i, p in enumerate(parsed[1:], start=1):
            if p == '-f':
                params['cow'] = parsed[i + 1]
            elif p == '-e':
                params['eyes'] = parsed[i + 1]
            elif p == '-T':
                params['tongue'] = parsed[i + 1]
        return params

    def do_cowsay(self, args):
        """Calls cowsay from cowsay, usage: cowsay message [--f cow] [--eyes eye_string] [--T tongue_string] [-W width] [-n]

        Params:
            message: Empty by default
            cow: -f – the available cows can be found by calling list_cows
            eyes: -e or eye_string: Select the appearance of the cow\'s eyes. The first two characters will be used
            tongue: -T or tongue_string: Select cow tongue. Must be two chars long
            width: -W: Message wrap width
            wrap_text: -n: To wrap the message
        """
        params = self._get_cowsay_params(args)
        print(cowsay(**params))

    def do_cowthink(self, args):
        """Calls cowthink from cowsay, usage: cowsay message [-f cow] [-e eye_string] [-T tongue_string] [-W width] [-n]
        
        Params:
            message: The message to de displayed
            cow: -f – the available cows can be found by calling `list_cows`:
            eyes: -e or eye_string: Select the appearance of the cow\'s eyes. The first two characters will be used
            tongue: -T or tongue_string: Select cow tongue. Must be two chars long
            width: -W: Message wrap width
            wrap_text: -n: To wrap the message
        """
        params = self._get_cowsay_params(args)
        print(cowthink(**params))

    def do_make_bubble(self, args):
        """Call make_bubble from cowsay, usage: make_bubble message [--brackets "Bubble('o', '(', ')', '(', ')', '(', ')', '(', ')')"] [-W 40] [-n]
        
        Params:
            message: Empty by default
            width: -W: Wrap width
            wrap_text: -n: To wrap the message
        """
        parsed = self._get_parsed_with_default(args)
        params = {
            'text': parsed[0],
            'width': 40,
            'wrap_text': False
        }
        for i, p in enumerate(parsed[1:], start=1):
            if p == '-W':
                params['width'] = int(parsed[i + 1])
            elif p == '-n':
                params['wrap_text'] = True
        print(make_bubble(**params))

    def do_list_cows(self, args):
        """Print list of cows, usage: list_cows [file]"""
        if len(args) == 0:
            print(list_cows())
        else:
            file = shlex.split(args)[0]
            print(list_cows(file))

    def do_exit(self, args):
        return 1

cmdline = CommandLine()
cmdline.cmdloop()