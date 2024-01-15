from kivy.app import App
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
import os
import random
from kivy.config import Config

# Set the window to run in fullscreen mode
Config.set('graphics', 'fullscreen', 'auto')

class SlideshowApp(App):
    min_display_time = 20  # Minimum display time (seconds)
    max_display_time = 35  # Maximum display time (seconds)
    pictures_folder = "/storage/emulated/0/Pictures"  # Updated picture folder path
    
    def build(self):
        # Check if the specified folder exists
        if not os.path.exists(self.pictures_folder):
            print("Pictures folder not found. Please ensure your pictures are in the specified folder.")
            return

        self.image_files = [f for f in os.listdir(self.pictures_folder) if f.lower().endswith('.jpg')]
        self.randomize_order()
        self.current_image_index = 0
        self.image = Image(allow_stretch=True)

        # Schedule the initial display
        self.show_current_image()
        Clock.schedule_once(self.next_image, random.uniform(self.min_display_time, self.max_display_time))

        return self.image

    def randomize_order(self):
        random.shuffle(self.image_files)

    def show_current_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            image_path = os.path.join(self.pictures_folder, self.image_files[self.current_image_index])
            self.image.source = image_path

    def next_image(self, dt):
        fade_out_animation = Animation(opacity=0, duration=1.0)
        fade_out_animation.bind(on_complete=self.load_next_image)
        fade_out_animation.start(self.image)

    def load_next_image(self, widget, *args):
        self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
        self.show_current_image()
        self.randomize_order()
        fade_in_animation = Animation(opacity=1, duration=1.0)
        fade_in_animation.start(self.image)

        Clock.schedule_once(self.fade_out, random.uniform(self.min_display_time, self.max_display_time))

    def fade_out(self, dt):
        fade_out_animation = Animation(opacity=0, duration=1.0)
        fade_out_animation.bind(on_complete=self.load_next_image)
        fade_out_animation.start(self.image)

if __name__ == '__main__':
    SlideshowApp().run()
