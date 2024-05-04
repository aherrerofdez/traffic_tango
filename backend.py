class Back(object):
    def __init__(self):
        pass

    @staticmethod
    def get_instructions():
        # Static method to get instructions for playing the game
        instructions = '1. Choosing a Mode: \n     - User Mode: if you want to play the game. \n     - Computer Mode:' \
                       ' if you want to watch our AI play. \n \n 2. Choosing a Difficulty Level: \n You can choose ' \
                       'any level among Easy, Medium and Difficult. \n \n 3. Click on "PLAY" to start playing. You ' \
                       'can use the arrows in your keyboard or the ones in the screen. \n \n 4. Click on "EXIT" if ' \
                       'you want to close the game.'
        return instructions

    @staticmethod
    def get_track(index):
        # Static method to get track parameters based on difficulty level
        # Default Mode: Medium
        length = 0.9
        speed = 12
        if index == 0:
            # Easy Mode
            length = 1
            speed = 15
        if index == 2:
            # Difficult Mode
            length = 0.5
            speed = 8
        params = [speed, length]
        return params
