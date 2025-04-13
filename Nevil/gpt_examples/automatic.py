import random
import time
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning, module="ALSA")

# Actions: forward, backward, left, right, stop, circle left, circle right, come here, shake head, 
#    nod, wave hands, resist, act cute, rub hands, think, twist body, celebrate, depressed, keep think
#
# Sounds: honk, start engine

# -----------------------
# Main Auto Class
# -----------------------
class Automatic:
    
    # -----------------------
    # Mood Profiles (Expanded)
    # -----------------------
    MOOD_PROFILES = {
        "playful":     {"volume": 85, "curiosity": 70, "sociability": 90, "whimsy": 95, "energy": 90},
        "brooding":    {"volume": 25, "curiosity": 40, "sociability": 10, "whimsy": 15, "energy": 30},
        "curious":     {"volume": 40, "curiosity": 85, "sociability": 50, "whimsy": 35, "energy": 60},
        "melancholic": {"volume": 30, "curiosity": 30, "sociability": 20, "whimsy": 20, "energy": 20},
        "zippy":       {"volume": 70, "curiosity": 60, "sociability": 60, "whimsy": 50, "energy": 95},
        "lonely":      {"volume": 60, "curiosity": 40, "sociability": 80, "whimsy": 20, "energy": 50},
        "mischievous": {"volume": 90, "curiosity": 75, "sociability": 50, "whimsy": 95, "energy": 85},
        "sleepy":      {"volume": 10, "curiosity": 20, "sociability": 10, "whimsy": 5,  "energy": 15}
    }

    # -----------------------
    # Base Behavior Weights
    # -----------------------
    BEHAVIOR_BASE_WEIGHTS = {
        "explore": 0.3,
        "rest": 0.1,
        "sleep": 0.1,
        "fidget": 0.0,
        "address": 0.0,
        "play": 0.2,
        "panic": 0.05,
        "circle": 0.05,
        "sing": 0.05,
        "mutter": 0.05,
        "dance": 0.1
    }

    # -----------------------
    # Trait Biases for Weight Calculation
    # -----------------------
    BEHAVIOR_TRAIT_BIASES = {
        "explore":     {"curiosity": 1.2, "energy": 1.1},
        "rest":        {"energy": 0.6},
        "sleep":       {"energy": 0.3},
        "fidget":      {"whimsy": 1.2, "energy": 0.8},
        "address":     {"sociability": 1.4},
        "play":        {"whimsy": 1.2, "energy": 1.2},
        "panic":       {"energy": 1.5},
        "circle":      {"curiosity": 1.1, "energy": 1.1},
        "sing":        {"whimsy": 1.3},
        "mutter":      {"curiosity": 0.7, "sociability": 0.6},
        "dance":       {"energy": 1.3, "whimsy": 1.5}
    }

    # -----------------------
    # Behavior Functions
    # -----------------------
    def __init__(self, gpt_car_self):
        self.current_mood_name = "curious"  # Default mood
        self.current_mood = self.MOOD_PROFILES[self.current_mood_name]
        self.car_self = gpt_car_self  # Store the gpt_car's self
        
        # Map behavior names to their functions
        self.BEHAVIOR_FUNCTIONS = {
            "explore": self.explore,
            "rest": self.rest,
            "sleep": self.sleep,
            "fidget": self.fidget,
            "address": self.address,
            "play": self.play,
            "panic": self.panic,
            "circle": self.circle,
            "sing": self.sing,
            "mutter": self.mutter,
            "dance": self.dance
        }

    def do_action(self, action_str, mood=None):
        print(f"[action] {action_str}" + (f" ({mood})" if mood else ""))
        action, params = self.car_self.parse_action(action_str)  # Use gpt_car's parse_action
        if action in self.car_self.ACTIONS:  # Use gpt_car's ACTIONS
            if params:
                self.car_self.ACTIONS[action](self.car_self.my_car, *params)
            else:
                self.car_self.ACTIONS[action](self.car_self.my_car)

    def explore(self, mood):
        actions = []
        curiosity = mood["curiosity"]
        energy = mood["energy"]
        whimsy = mood["whimsy"]

        speed = int(15 + energy * 0.3)
        distance = int(10 + curiosity * 0.2)
        actions.append(f"forward {distance} {speed}")

        if curiosity > 60:
            actions.append("circle left")
            actions.append("sleep 0.3")
            actions.append("circle right")
            actions.append("sleep 0.3")

        if whimsy > 75:
            actions.append("nod")

        for action in actions:
            self.do_action(action, mood="exploring")

    def rest(self, mood):
        actions = []
        energy = mood["energy"]
        duration = (100 - energy) / 20
        actions.append("act cute")
        actions.append(f"sleep {duration}")
        
        for action in actions:
            self.do_action(action, mood="peaceful")

    def sleep(self, mood):
        actions = []
        energy = mood["energy"]
        duration = (100 - energy) / 8
        actions.append("depressed")
        actions.append(f"sleep {duration}")
        
        for action in actions:
            self.do_action(action, mood="sleepy")

    def fidget(self, mood):
        actions = []
        energy = mood["energy"]
        whimsy = mood["whimsy"]

        if energy < 30:
            actions.append("twist body")
        else:
            actions.append("shake head")

        if whimsy > 60:
            actions.append("nod")

        actions.append("sleep 0.8")

        for action in actions:
            self.do_action(action, mood="restless")

    def address(self, mood):
        actions = []
        sociability = mood["sociability"]
        curiosity = mood["curiosity"]

        if sociability > 50:
            actions.append("wave hands")
            if curiosity > 40:
                actions.append("think")
            else:
                actions.append("nod")
        else:
            actions.append("resist")

        actions.append("sleep 1.0")

        for action in actions:
            self.do_action(action, mood="alert")

    def play(self, mood):
        actions = []
        energy = mood["energy"]
        whimsy = mood["whimsy"]

        actions.append("circle left")
        
        if whimsy > 60:
            actions.append("wave hands")

        if mood["volume"] > 70:
            actions.append("honk")

        actions.append("sleep 1.0")

        for action in actions:
            self.do_action(action, mood="playful")

    def panic(self, mood):
        actions = []
        energy = mood["energy"]
        volume = mood["volume"]

        speed = min(50, int(30 + energy * 0.5))
        actions.append(f"backward {speed} 10")

        if volume > 50:
            actions.append("honk")

        actions.append("circle right")
        actions.append("sleep 1.0")

        for action in actions:
            self.do_action(action, mood="alarmed")

    def circle(self, mood):
        actions = []
        curiosity = mood["curiosity"]
        energy = mood["energy"]

        actions.append("circle right")
        
        if curiosity > 70:
            actions.append("think")

        actions.append("sleep 1.2")

        for action in actions:
            self.do_action(action, mood="focused")

    def sing(self, mood):
        actions = []
        volume = mood["volume"]
        whimsy = mood["whimsy"]

        if volume > 60:
            actions.append("celebrate")
        else:
            actions.append("act cute")

        if whimsy > 70:
            actions.append("wave hands")

        actions.append("sleep 2.0")

        for action in actions:
            self.do_action(action)

    def mutter(self, mood):
        actions = []
        sociability = mood["sociability"]
        curiosity = mood["curiosity"]

        if sociability < 30:
            actions.append("keep think")
        else:
            actions.append("think")

        if curiosity > 50:
            actions.append("rub hands")

        actions.append("sleep 1.0")

        for action in actions:
            self.do_action(action, mood="brooding")

    def dance(self, mood):
        actions = []
        energy = mood["energy"]
        whimsy = mood["whimsy"]

        if whimsy > 50:
            actions.append("twist body")
        else:
            actions.append("wave hands")

        if mood["volume"] > 60:
            actions.append("celebrate")

        actions.append("sleep 1.5")

        for action in actions:
            self.do_action(action, mood="groovy")

    def run_idle_loop(self, cycles=3):
        for _ in range(cycles):
            print(f"\n[auto] Mood: {self.current_mood_name}")
            weights = self.compute_behavior_weights(
                self.BEHAVIOR_BASE_WEIGHTS,
                self.current_mood,
                self.BEHAVIOR_TRAIT_BIASES
            )
            behavior_name = self.weighted_choice(weights)
            print(f"[auto] Chosen behavior: {behavior_name}")
            behavior_func = self.BEHAVIOR_FUNCTIONS.get(behavior_name)
            if behavior_func:
                behavior_func(self.current_mood)

    def get_mood_param_str(self):
        traits = self.current_mood
        return f"mood={self.current_mood_name} volume={traits['volume']} curiosity={traits['curiosity']} sociability={traits['sociability']} whimsy={traits['whimsy']} energy={traits['energy']}"

    # -----------------------
    # Weight Calculation
    # -----------------------
    def compute_behavior_weights(self, base_weights, mood_profile, trait_biases):
        adjusted = {}
        for behavior, base_weight in base_weights.items():
            trait_influences = trait_biases.get(behavior, {})
            modifier = 1.0
            for trait, influence in trait_influences.items():
                trait_val = max(mood_profile.get(trait, 50) / 50, 0.01)
                modifier *= trait_val ** (influence - 1)
            adjusted[behavior] = base_weight * modifier
        return adjusted

    def weighted_choice(self, weight_dict):
        choices, weights = zip(*weight_dict.items())
        return random.choices(choices, weights=weights, k=1)[0]

    def pick_random_mood(self):
        name = random.choice(list(self.MOOD_PROFILES.keys()))
        return name, self.MOOD_PROFILES[name]

    def set_mood(self, mood_name):
        if mood_name in self.MOOD_PROFILES:
            self.current_mood_name = mood_name
            self.current_mood = self.MOOD_PROFILES[mood_name].copy()
            # Perform transition behavior
            self.mood_transition()
            return True
        return False

    def mood_transition(self):
        """Perform a transition behavior when mood changes"""
        actions = []
        if self.current_mood["energy"] > 70:
            actions.append("celebrate")
        elif self.current_mood["energy"] < 30:
            actions.append("depressed")
        else:
            actions.append("think")
        
        for action in actions:
            self.do_action(action, mood=f"transitioning to {self.current_mood_name}")

    def get_cycle_count(self):
        # Use energy and whimsy to determine number of cycles
        energy = self.current_mood.get("energy", 50)
        whimsy = self.current_mood.get("whimsy", 50)
        
        # More energy/whimsy = more likely to do more cycles
        base_cycles = random.randint(2, 10)
        mood_factor = (energy + whimsy) / 100  # 0 to 2 range
        cycles = max(2, min(10, int(base_cycles * mood_factor)))
        
        print(f"[system] Feeling {'energetic' if mood_factor > 1 else 'mellow'}, doing {cycles} cycles")
        return cycles
