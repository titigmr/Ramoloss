import discord


class ParseArgs:
    def __init__(self):
        pass

    def find_title(self, message):
        first = message.find('{') + 1
        last = message.find('}')
        if first == 0 or last == -1:
            return "Not using the command correctly"
        return message[first:last]

    def find_options(self, message, options, n_min=2):
        first = message.find('[') + 1
        last = message.find(']')
        if (first == 0 or last == -1):
            if len(options) < n_min:
                return "Not using the command correctly"
            else:
                return options
        options.append(message[first:last])
        message = message[last+1:]
        return self.find_options(message, options)