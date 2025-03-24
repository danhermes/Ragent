from openai_helper import OpenAiHelper
#from keys import OPENAI_API_KEY, OPENAI_ASSISTANT_ID
from action_helper import actions_dict, sounds_dict, move_forward_this_way as forward, move_backward_this_way as backward, turn_left_in_place, turn_right_in_place, turn_left, turn_right, stop, shake_head, nod, wave_hands, resist, act_cute, rub_hands, think, keep_think, twist_body, celebrate, depressed
from utils import *
from robot_hat import TTS
import readline # optimize keyboard input, only need to import
import speech_recognition as sr
import os
import sys
from dotenv import load_dotenv
from time import sleep  # Add this import

# Load environment variables from .env file
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from picarx import Picarx
from robot_hat import Music, Pin
import time
import threading
import random
from get_topics import GetTopics

class PiCar:
    def __init__(self):
        try:
            # First try to cleanup any existing resources
            from robot_hat import reset_mcu
            reset_mcu()
            time.sleep(0.1)
            
            self.init_system()
            self.init_input_mode()
            self.init_openai()
            self.init_car()
            self.init_camera()
            self.init_speech()
            self.init_sound_effects()
            self.init_threads()
            self.init_topics()
            self.init_movement()
        except Exception as e:
            print(f"Initialization error: {e}")
            raise

    def init_system(self):
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        os.popen("pinctrl set 20 op dh")  # enable robot_hat speaker switch
        self.current_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.current_path)
        self.tts = TTS()

    def init_input_mode(self):
        self.input_mode = 'voice'
        self.with_img = True
        args = sys.argv[1:]
        if '--keyboard' in args:
            self.input_mode = 'keyboard'
        if '--no-img' in args:
            self.with_img = False

    def init_openai(self):
        self.openai_helper = OpenAiHelper(
            os.getenv("OPENAI_API_KEY"), 
            os.getenv("OPENAI_ASSISTANT_ID"), 
            'picarx'
        )
        self.LANGUAGE = "en"
        self.VOLUME_DB = 3
        self.TTS_VOICE = 'onyx'

    def init_car(self):
        try:
            self.my_car = Picarx()
            # Add safety distance attributes
            self.my_car.SafeDistance = 30  # 30cm safe distance
            self.my_car.DangerDistance = 15  # 15cm danger distance
            self.my_car.speed = 30  # Set default speed
            time.sleep(1)
        except Exception as e:
            raise RuntimeError(e)
        self.music = Music()
        self.led = Pin('LED')
        self.DEFAULT_HEAD_TILT = 20

    def init_camera(self):
        gray_print("Initializing camera...")
        if not self.with_img:
            gray_print("Camera disabled, skipping initialization")
            return
            
        try:
            gray_print("Importing camera libraries...")
            from vilib import Vilib
            import cv2
            # Store these for later use
            self.Vilib = Vilib
            self.cv2 = cv2

            gray_print("Starting camera...")
            Vilib.camera_start(vflip=False, hflip=False)
            Vilib.show_fps()
            gray_print("Setting up web display...")
            Vilib.display(local=False, web=True)

            gray_print("Waiting for Flask server to start...")
            while True:
                if Vilib.flask_start:
                    break
                time.sleep(0.01)
            time.sleep(.5)
            gray_print("Camera initialization complete\n")
        except Exception as e:
            gray_print(f"Camera initialization failed: {str(e)}")
            raise

    def init_speech(self):
        self.recognizer = sr.Recognizer()
        # More moderate energy threshold for noisy environments
        self.recognizer.energy_threshold = 300  # Make it adjust more quickly to background noise
        self.recognizer.dynamic_energy_adjustment_damping = 0.1  # Default 0.16, lower means faster adjustment
        self.recognizer.dynamic_energy_ratio = 1.7  # Default 1.6, increase for better noise handling
        self.recognizer.pause_threshold = 2  # Shorter pause threshold to detect end of speech faster
        self.recognizer.operation_timeout = 10  #None     No timeout
        
        # Speech handler variables
        self.speech_loaded = False
        self.speech_lock = threading.Lock()
        self.tts_file = None

    def init_sound_effects(self):
        self.SOUND_EFFECT_ACTIONS = ["honking", "start engine"]
        self.sound_effects_queue = []

    def init_threads(self):
        # Action thread variables
        self.action_status = 'standby'
        self.led_status = 'standby'
        self.last_action_status = 'standby'
        self.last_led_status = 'standby'
        self.LED_DOUBLE_BLINK_INTERVAL = 0.8
        self.LED_BLINK_INTERVAL = 0.1
        self.actions_to_be_done = []
        self.action_lock = threading.Lock()

        # Create and start threads
        self.speak_thread = threading.Thread(target=self.speech_handler)
        self.speak_thread.daemon = True
        self.speak_thread.start()  # Actually start the thread
        
        self.action_thread = threading.Thread(target=self.action_handler)
        self.action_thread.daemon = True
        self.action_thread.start()  # Actually start the thread

    def init_topics(self):
        self.topics = GetTopics().get_topics()

    def init_movement(self):
        self.ACTIONS = actions_dict

    def play_audio(self, music, tts_file):
        try:
            if os.path.exists(tts_file):
                music.music_play(tts_file)
                while music.pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                music.music_stop()  # Stop the music explicitly
                music.pygame.mixer.quit()  # Release the audio device
                music.pygame.mixer.init()  # Reinitialize for next use
                os.remove(tts_file)
        except Exception as e:
            print(f"Error playing TTS: {e}")

    def speech_handler(self): #Speech thread: audio loop waiting for speech_loaded to be true
        while True:
            with self.speech_lock:
                _isloaded = self.speech_loaded

            if _isloaded:   
                gray_print("Speech loaded, handling it!!!")             
                # Handle sound effects first
                _sound_effects = list(self.sound_effects_queue)  # Get copy of queue
                self.sound_effects_queue.clear()  # Clear queue
                if _sound_effects:
                    gray_print(f"Playing sound effects: {_sound_effects}")
                    for sound in _sound_effects:
                        try:
                            gray_print(f"  Playing sound: {sound}")
                            sounds_dict[sound](self.music)
                        except Exception as e:
                            print(f'Sound effect error: {e}')
                    
                # Then handle TTS
                gray_print(f"Playing TTS file: {self.tts_file}")
                self.play_audio(self.music, self.tts_file)
                gray_print("TTS playback complete")
                with self.speech_lock:
                    self.speech_loaded = False
            
            time.sleep(0.05)

    def handle_led_status(self, state, last_led_time):
        """Handle LED behavior based on current state"""
        if self.led_status != self.last_led_status:
            last_led_time = 0
            self.last_led_status = self.led_status

        if state == 'standby':
            if time.time() - last_led_time > self.LED_DOUBLE_BLINK_INTERVAL:
                self.led.off()
                self.led.on()
                sleep(.1)
                self.led.off()
                sleep(.1)
                self.led.on()
                sleep(.1)
                self.led.off()
                return time.time()
        elif state == 'think':
            if time.time() - last_led_time > self.LED_BLINK_INTERVAL:
                self.led.off()
                sleep(self.LED_BLINK_INTERVAL)
                self.led.on()
                sleep(self.LED_BLINK_INTERVAL)
                return time.time()
        elif state == 'actions':
            self.led.on()
        
        return last_led_time

    def parse_action(self, response):
        parts = response.lower().split()
        if len(parts) >= 2:
            # Handle forward movement
            if parts[0] == "forward":
                try:
                    distance = int(parts[1])
                    speed = int(parts[2]) if len(parts) > 2 else None
                    gray_print(f"Parsed forward movement: distance={distance}cm" + 
                             (f", speed={speed}" if speed else " with default speed"))
                    return "forward", [distance, speed] if speed else [distance]
                except (IndexError, ValueError):
                    gray_print(f"Failed to parse forward parameters from: {parts}")
                    return None, None
            
            # Handle backward movement
            elif parts[0] == "backward":
                try:
                    distance = int(parts[1])
                    speed = int(parts[2]) if len(parts) > 2 else None
                    gray_print(f"Parsed backward movement: distance={distance}cm" + 
                             (f", speed={speed}" if speed else " with default speed"))
                    return "backward", [distance, speed] if speed else [distance]
                except (IndexError, ValueError):
                    gray_print(f"Failed to parse backward parameters from: {parts}")
                    return None, None
        
        # Handle other actions
        return response, None

    def action_handler(self): #Action thread: action loop waiting for action_status to be actions
        standby_actions = ['act cute', 'nod', 'depressed']
        standby_weights = [1, 0.3, 0.1]
        action_interval = 20 # seconds
        last_action_time = time.time()
        last_led_time = time.time()

        while True: # the action loop
            with self.action_lock:
                _state = self.action_status # the signal to execute actions
            
            # led
            # ------------------------------
            self.led_status = _state
            last_led_time = self.handle_led_status(_state, last_led_time)

            # actions
            # ------------------------------
            if _state == 'standby':
                if self.last_action_status != 'standby':
                    gray_print("Entering standby state")
                self.last_action_status = 'standby'
                if time.time() - last_action_time > action_interval:
                    last_action_time = time.time()
                    action_interval = random.randint(8, 40)
                    _standby_action = random.choices(standby_actions, weights=standby_weights)[0]
                    gray_print(f"Performing standby action: {_standby_action}")
                    self.ACTIONS[_standby_action](self.my_car)

            elif _state == 'think':
                if self.last_action_status != 'think':
                    gray_print("Entering think state")
                    self.last_action_status = 'think'
                    self.ACTIONS["think"](self.my_car)

            elif _state == 'actions':
                if self.last_action_status != 'actions':
                    gray_print("Entering actions state")
                self.last_action_status = 'actions'
                with self.action_lock:
                    gray_print(f'actionsT: {self.actions_to_be_done}')
                    _actions = self.actions_to_be_done
                for _action in _actions:
                    try:
                        gray_print(f'actionT: {_action}')
                        #if _action in self.ACTIONS:
                        gray_print(f"Performing action: {_action}")
                        action, params = self.parse_action(_action)
                        if action in self.ACTIONS:
                            if params:
                                self.ACTIONS[action](self.my_car, *params)
                            else:
                                self.ACTIONS[action](self.my_car)
                    except Exception as e:
                        print(f'action error: {e}')
                    time.sleep(0.5)

                gray_print("Actions complete, setting status to actions_done")
                with self.action_lock:
                    self.action_status = 'actions_done'
                last_action_time = time.time()

            time.sleep(0.01)

    def main(self):
        self.my_car.reset()
        self.my_car.set_cam_tilt_angle(self.DEFAULT_HEAD_TILT)

        while True:
            if self.input_mode == 'voice':
                self.my_car.set_cam_tilt_angle(self.DEFAULT_HEAD_TILT)

                # listen
                # ----------------------------------------------------------------
                gray_print("listening ...")

                with self.action_lock:
                    self.action_status = 'standby'

                listen_start = time.time()
                _stderr_back = redirect_error_2_null()
                with sr.Microphone(chunk_size=8192) as source:
                    cancel_redirect_error(_stderr_back)
                    self.recognizer.adjust_for_ambient_noise(source)
                    audio = self.recognizer.listen(source)
                gray_print(f"Listen time: {time.time() - listen_start:.3f}s")

                # stt
                # ----------------------------------------------------------------
                stt_start = time.time()
                _result = self.openai_helper.stt(audio, language=self.LANGUAGE)
                gray_print(f"STT time: {time.time() - stt_start:.3f}s")

                if _result == False or _result == "":
                    print() # new line
                    continue

            elif self.input_mode == 'keyboard':
                self.my_car.set_cam_tilt_angle(self.DEFAULT_HEAD_TILT)

                with self.action_lock:
                    self.action_status = 'standby'

                _result = input(f'\033[1;30m{"intput: "}\033[0m').encode(sys.stdin.encoding).decode('utf-8')

                if _result == False or _result == "":
                    print() # new line
                    continue

            else:
                raise ValueError("Invalid input mode")

            # chat-gpt
            # ---------------------------------------------------------------- 
            gpt_start = time.time()

            with self.action_lock:
                self.action_status = 'think'

            if self.with_img:
                img_path = './img_imput.jpg'
                cv2_start = time.time()
                self.cv2.imwrite(img_path, self.Vilib.img)
                gray_print(f"Image capture time: {time.time() - cv2_start:.3f}s")
                response = self.openai_helper.dialogue_with_img(_result, img_path)
            else:
                response = self.openai_helper.dialogue(_result)

            gray_print(f'GPT total time: {time.time() - gpt_start:.3f}s')

            # Parse actions, answer, and sound actions
            # ----------------------------------------------------------------
            parse_start = time.time()
            _sound_actions = [] 
            try:
                if isinstance(response, dict):
                    gray_print(f'response-isinstance1: {response}')
                    if 'actions' in response:
                        actions = list(response['actions'])
                    else:
                        actions = ['stop']
                    gray_print(f'actions-isinstance1: {actions}')
                    if 'answer' in response:
                        answer = response['answer']
                    else:
                        answer = ''
                    gray_print(f'answer-isinstance1: {answer}')
                    if len(answer) > 0:
                        _actions = list.copy(actions)
                        gray_print(f'_actions-isinstance2: {_actions}')
                        for _action in _actions:
                            if _action in self.SOUND_EFFECT_ACTIONS:
                                _sound_actions.append(_action)
                                actions.remove(_action)
                    gray_print(f'answer2: {answer}')
                    gray_print(f'actions-isinstance2: {actions}')
                    gray_print(f'sound actions2: {_sound_actions}')
                else:
                    response = str(response)
                    if len(response) > 0:
                        actions = []
                        answer = response
            except Exception as e:
                gray_print(f"Response parsing error: {str(e)}")
                actions = []
                answer = ''
            gray_print(f"Parse time: {time.time() - parse_start:.3f}s")
            
            # TTS
            # ----------------------------------------------------------------
            tts_start = time.time()
            try:
                _tts_status = False
                if answer != '':
                    _time = time.strftime("%y-%m-%d_%H-%M-%S", time.localtime())
                    _tts_f = f"./tts/{_time}_raw.wav"
                    
                    _tts_status = self.openai_helper.text_to_speech(answer, _tts_f, self.TTS_VOICE, response_format='wav')
                
                    if _tts_status:
                        self.tts_file = f"./tts/{_time}_{self.VOLUME_DB}dB.wav"
                        _tts_status = sox_volume(_tts_f, self.tts_file, self.VOLUME_DB)
                gray_print(f'TTS generation time: {time.time() - tts_start:.3f}s')

                # Actions
                # ----------------------------------------------------------------
                action_start = time.time()
                with self.action_lock:
                    self.actions_to_be_done = actions
                    gray_print(f'actions: {self.actions_to_be_done}')
                    self.action_status = 'actions'

                # Speech and sound effects
                # ----------------------------------------------------------------
                for _sound in _sound_actions:
                    with self.speech_lock:
                        self.sound_effects_queue.append(_sound)

                if _tts_status:
                    with self.speech_lock:
                        self.speech_loaded = True

                print() # new line

            except Exception as e:
                print(f'actions or TTS error: {e}')
            
            # Wait for speech and actions to complete
            # ----------------------------------------------------------------
            wait_start = time.time()
            if _tts_status:
                while True:
                    with self.speech_lock:
                        if not self.speech_loaded:
                            break
                    time.sleep(.01)

            while True:
                with self.action_lock:
                    if self.action_status != 'actions':
                        break
                time.sleep(.01)
            gray_print(f"Wait time for completion: {time.time() - wait_start:.3f}s")
            gray_print(f"Total iteration time: {time.time() - listen_start:.3f}s\n")

    def cleanup(self):
        """Add this method for cleanup"""
        if hasattr(self, 'my_car'):
            self.my_car.reset()
        from robot_hat import reset_mcu
        reset_mcu()

if __name__ == "__main__":
    car = None
    try:
        car = PiCar()
        car.main()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        if car:
            car.cleanup()  # Add cleanup call

