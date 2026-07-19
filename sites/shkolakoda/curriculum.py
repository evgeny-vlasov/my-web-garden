TOPICS = {
    "coordinates": {
        "title": "Coordinates and Movement",
        "endpoint": "coordinates_topic",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "intro": (
            "Coordinates describe position. A screen is a map made from numbers, "
            "and every object needs a way to answer: Where am I?"
        ),
        "meta_description": (
            "Learn how x and y coordinates describe position and movement in Scratch, "
            "games, maps, animation, and later robotics work."
        ),
        "math_kernel": [
            ("Number lines", "A coordinate uses a number line in each direction."),
            ("Positive and negative", "The sign tells us which side of the origin a point occupies."),
            ("Horizontal and vertical", "The x value controls left and right; y controls down and up."),
            ("Change in position", "Distance moved can be described by comparing a before and after value."),
            ("Centre and origin", "The point x: 0, y: 0 gives the screen a shared reference point."),
        ],
        "common_mistakes": [
            ("Changing x instead of y", "The character moves sideways when the intended movement was vertical."),
            ("Using the wrong sign", "A positive change moves in the opposite direction from the one predicted."),
            ("Starting from an unknown position", "A test gives different results because the sprite was never reset."),
            ("Moving forever", "The code changes position repeatedly without checking stage boundaries."),
            ("Confusing direction with position", "Where a sprite faces is not the same as where it is located."),
            ("Fixing the symptom", "Extra movement blocks hide a problem instead of inspecting the current x and y values."),
        ],
        "returns_later": [
            ("Games", "Place players, targets, obstacles, projectiles, and safe zones."),
            ("Maps", "Describe locations and plan movement between them."),
            ("Animation", "Move an object from one known position to another over time."),
            ("Robot navigation", "Represent where a robot is and where it should go."),
            ("Drones", "Track position while controlling movement in more dimensions."),
            ("Computer vision", "Locate objects inside an image using measured positions."),
            ("Screen layouts", "Place interface elements consistently across a digital space."),
        ],
        "program_appearances": [
            ("Scratch", "Active now", "active", "scratch"),
            ("Robotics", "Active now", "active", "robotics"),
            ("Roblox", "Available later", "later", "roblox"),
            ("AI and computer vision", "Available later", "later", "ai"),
        ],
        "parent_note": (
            "A chase game may look like pure entertainment, but underneath it, "
            "students are learning to represent position with numbers, predict "
            "movement, test boundaries, and debug cause and effect."
        ),
    }
}


LESSONS = {
    "coordinates-and-movement": {
        "title": "How Does the Screen Know Where You Are?",
        "endpoint": "coordinates_lesson",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "topic": "Coordinates and Movement",
        "topic_endpoint": "coordinates_topic",
        "duration": "90 minutes",
        "age_language": "Beginner-friendly; challenge depth can be adjusted for the group.",
        "meta_description": (
            "A public School of Code Scratch lesson on reading x and y coordinates, "
            "predicting movement, checking boundaries, and debugging position."
        ),
        "story": (
            "A giant pigeon is chasing your character across Calgary. The computer "
            "cannot see the chase the way a person does. How does it know where the "
            "player is, where the pigeon is, or whether they have collided?"
        ),
        "timeline": [
            ("0-10 min", "Problem and story", "Turn a ridiculous chase into a precise position problem."),
            ("10-30 min", "Coordinates and movement", "Read x and y, predict changes, and reset to the origin."),
            ("30-65 min", "Guided build", "Build the core movement and chase systems together."),
            ("65-80 min", "Modification challenge", "Change one rule and test the consequences."),
            ("80-90 min", "Demonstration and explanation", "Show the system and explain its numbers."),
        ],
        "learning_goals": [
            "Read x and y positions.",
            "Move a sprite horizontally and vertically.",
            "Set a known starting position.",
            "Predict the result of coordinate changes.",
            "Recognize screen boundaries.",
            "Use position information while debugging.",
            "Explain movement using numbers.",
        ],
        "theory_examples": [
            ("change x by 20", "move right"),
            ("change x by -20", "move left"),
            ("change y by 20", "move up"),
            ("change y by -20", "move down"),
            ("go to x: 0 y: 0", "return to the centre"),
        ],
        "checkpoints": [
            "Student can identify the centre.",
            "Student can predict four movements before running them.",
            "Student can reset the player to a known position.",
            "Student can explain one bug using x or y.",
            "Student has changed at least one rule independently.",
        ],
        "challenge_levels": [
            {
                "name": "Builder",
                "ideas": ["Add screen wrapping.", "Add a second safe zone."],
            },
            {
                "name": "Inventor",
                "ideas": ["Create a temporary turbo move.", "Add a boundary warning."],
            },
            {
                "name": "Boss Level",
                "ideas": ["Optionally make pigeon speed depend on approximate distance."],
            },
        ],
        "demonstration_questions": [
            "What did you build?",
            "Which number controls left and right?",
            "Which number controls up and down?",
            "What went wrong?",
            "What did you change?",
        ],
        "parent_summary": (
            "Today students practised reading x and y coordinates, predicting movement, "
            "resetting a program to a known starting state, checking screen boundaries, "
            "and using position values to explain and repair bugs. The chase-game story "
            "made the work visible, but the underlying lesson was mathematical and logical."
        ),
    }
}


PROJECT_DETAILS = {
    "escape-from-the-giant-pigeon": {
        "name": "Escape from the Giant Pigeon",
        "endpoint": "giant_pigeon_project",
        "mode": "guided",
        "project_type": "Guided Class Project",
        "type_class": "guided",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "topic": "Coordinates and Movement",
        "topic_endpoint": "coordinates_topic",
        "difficulty": "Beginner / Builder",
        "estimated_time": "45-70 minutes",
        "topics": ["Coordinates", "Movement", "Conditions", "Collision", "Game State", "Debugging"],
        "meta_description": (
            "Build Escape from the Giant Pigeon, a guided Scratch chase project "
            "teaching coordinates, movement, collision, game state, and debugging."
        ),
        "mission": (
            "Reach a safe place while a huge, unreasonable pigeon chases you across the map. "
            "The game should be funny to play and precise enough to explain."
        ),
        "card_summary": (
            "Build a fast chase game with known positions, collision rules, "
            "win and loss states, and reliable restart behaviour."
        ),
        "what_students_build": [
            "Keyboard movement in four directions",
            "Known starting positions",
            "A pursuing pigeon",
            "One or more safe areas",
            "Collision or touch rules",
            "Clear win and loss states",
            "Restart behaviour that resets the whole system",
        ],
        "what_students_learn": [
            "x and y position",
            "movement as change",
            "starting state",
            "repeated checking",
            "collision",
            "conditions",
            "testing",
            "debugging",
        ],
        "needs": [
            "A browser",
            "The Scratch editor",
            "A keyboard",
            "A student-drawn character or ordinary built-in Scratch assets",
        ],
        "needs_note": (
            "No installation is required where browser-based Scratch is available. "
            "Saving and sharing options depend on account and classroom setup; account "
            "creation is not assumed by this project."
        ),
        "build_steps": [
            {
                "title": "Create the player",
                "task": "Choose or draw a character that is easy to see against the map.",
                "explanation": "The player is the object whose position the keyboard will change.",
                "checkpoint": "The player is visible and selected in the editor.",
                "mistake": "Editing the stage or pigeon when you meant to edit the player.",
            },
            {
                "title": "Set a known start",
                "task": "Choose a starting x and y position and reset the player there when the project begins.",
                "explanation": "A known start makes every test comparable.",
                "checkpoint": "Restarting always returns the player to the same place.",
                "mistake": "Moving the sprite by hand but never putting the starting position in code.",
            },
            {
                "title": "Add four-direction controls",
                "task": "Use keys to change x for left/right and y for down/up.",
                "explanation": "Movement is a controlled change in position.",
                "checkpoint": "Each key changes only the intended axis.",
                "mistake": "Changing y for a left/right key or using the wrong sign.",
            },
            {
                "title": "Add the giant pigeon",
                "task": "Draw or choose an ordinary bird-like sprite and give it a known starting point.",
                "explanation": "The pigeon is another object with its own coordinates.",
                "checkpoint": "The pigeon never starts directly on top of the player.",
                "mistake": "Leaving its starting position wherever the previous test ended.",
            },
            {
                "title": "Make the pigeon pursue",
                "task": "Make the pigeon repeatedly move toward the player using a simple pursuit rule.",
                "explanation": "The pursuer must check changing positions again and again.",
                "checkpoint": "The pigeon follows after the player moves.",
                "mistake": "Running the pursuit once instead of repeatedly.",
            },
            {
                "title": "Create a safe zone",
                "task": "Draw a clear destination and place it away from both starting positions.",
                "explanation": "A safe zone turns movement into a goal rather than wandering.",
                "checkpoint": "The player can reach it with the keyboard controls.",
                "mistake": "Placing it partly outside the stage or beneath another object.",
            },
            {
                "title": "Detect being caught",
                "task": "Repeatedly check whether the player touches the pigeon.",
                "explanation": "A condition changes the game when two objects collide.",
                "checkpoint": "Touching the pigeon produces a clear loss state.",
                "mistake": "Checking collision before play begins but never checking again.",
            },
            {
                "title": "Detect reaching safety",
                "task": "Check whether the player touches the safe zone and switch to a win state.",
                "explanation": "Win and loss are different states with different causes.",
                "checkpoint": "Reaching safety ends the chase visibly.",
                "mistake": "Allowing win and loss to trigger during the same moment without deciding priority.",
            },
            {
                "title": "Reset the whole game",
                "task": "Return positions, messages, and game state to their initial values.",
                "explanation": "Restart means restoring the system, not only moving the player.",
                "checkpoint": "Three restarts in a row behave the same way.",
                "mistake": "Resetting one sprite while the other keeps its old state.",
            },
            {
                "title": "Test strange situations",
                "task": "Try edges, rapid keys, simultaneous contact, and unusual starting arrangements.",
                "explanation": "Deliberate tests find assumptions hidden in otherwise working code.",
                "checkpoint": "Record and repair at least one surprising behaviour.",
                "mistake": "Only testing the easiest successful path.",
            },
        ],
        "pseudo_blocks": [
            "when green flag clicked\ngo to x: -180 y: -100",
            "if touching Giant Pigeon\n    switch state to CAUGHT",
        ],
        "test_questions": [
            "Can the player move in every direction?",
            "Does the player always begin in the same place?",
            "Can the player leave the stage unexpectedly?",
            "Can the pigeon begin on top of the player?",
            "Can both win and loss happen at once?",
            "Does restart truly reset everything?",
        ],
        "improvements": [
            "Try a different movement speed.",
            "Add multiple safe places.",
            "Add moving obstacles.",
            "Create a temporary shield.",
            "Add a pigeon mood meter.",
            "Draw a Calgary landmark-inspired map without protected logos or implied affiliations.",
            "Make pigeon behaviour increasingly dramatic while keeping the rules testable.",
        ],
        "challenge_levels": [
            {"name": "Builder", "description": "Add score or survival time."},
            {"name": "Inventor", "description": "Make the pigeon move differently when far away and near."},
            {"name": "Boss Level", "description": "Create two stages with different coordinate layouts."},
        ],
        "demonstrate": [
            "A known start",
            "Working x/y controls",
            "A win",
            "A loss",
            "One bug that was fixed",
            "One personal modification",
        ],
        "parent_explanation": (
            "The funny chase game develops coordinate reasoning, movement systems, "
            "conditions, game state, testing, and debugging. Students must represent "
            "position with numbers and explain how a change in code creates a change on screen."
        ),
    },
    "grandmas-intergalactic-taxi": {
        "name": "Grandma's Intergalactic Taxi",
        "endpoint": "grandmas_taxi_project",
        "mode": "lab",
        "project_type": "Computer Lab Project",
        "type_class": "lab",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "topic": "Coordinates and Movement",
        "topic_endpoint": "coordinates_topic",
        "difficulty": "Builder",
        "estimated_time": "45-90 minutes",
        "topics": ["Coordinates", "Movement", "Distance", "Sequences", "Score", "Boundaries", "Debugging"],
        "meta_description": (
            "Build Grandma's Intergalactic Taxi, a Scratch Computer Lab project "
            "using coordinates, routes, destinations, score, boundaries, and debugging."
        ),
        "mission": (
            "Grandma operates a taxi in space and has absolutely no intention of "
            "missing another pickup. Move between planets or stations using coordinates."
        ),
        "card_summary": (
            "Navigate a space taxi between coordinate-based pickups and destinations."
        ),
        "lab_note": (
            "This is not a complete teacher-led recipe. The required systems define "
            "the project, but students may draw different maps, choose different controls, "
            "and solve arrival and dispatch logic in more than one correct way."
        ),
        "required_systems": [
            "A space map with three or more destinations",
            "A controllable taxi",
            "Arrival detection at each destination",
            "Passenger pickup and delivery states",
            "A completed-trip counter",
            "A reset path after mistakes",
        ],
        "build_order": [
            "Draw the map and record useful destination coordinates.",
            "Place the taxi at a known start and build movement controls.",
            "Detect arrival at one station before adding the others.",
            "Create pickup and delivery states for one passenger.",
            "Track completed trips and reset the current request.",
            "Test boundaries, wrong destinations, and repeated arrivals.",
        ],
        "checkpoints": [
            "The taxi starts from a known position.",
            "At least three destinations have distinct locations.",
            "Pickup and delivery are different states.",
            "A trip cannot score repeatedly without a new request.",
            "The student can explain one route using x and y changes.",
        ],
        "challenge_cards": [
            "Fuel decreases with movement.",
            "Passenger destinations are randomized.",
            "A wrong station costs time.",
            "An asteroid zone changes the route.",
            "Coordinates appear as a navigation display.",
            "Create a shortest-route challenge.",
        ],
        "boss_level": (
            "Add a dispatch system that gives destinations in coordinate form, such as "
            "'Pickup requested near x: 140, y: -80.' The player must read the request "
            "and navigate without a flashing destination marker."
        ),
        "demonstrate": [
            "Three destinations on a coordinate map",
            "A complete pickup and delivery",
            "A trip counter that changes once per delivery",
            "Recovery from a wrong route or mistake",
            "One independently chosen challenge card",
        ],
        "parent_explanation": (
            "This project turns coordinate reading into map thinking and route planning. "
            "Students track changing positions, represent destinations, distinguish pickup "
            "from delivery state, test boundaries, and debug a system with several valid routes."
        ),
    },
    "astro-chicken-rescue": {
        "name": "Astro-Chicken Rescue",
        "endpoint": "astro_chicken_project",
        "mode": "lab",
        "project_type": "Computer Lab Project",
        "type_class": "lab",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "topic": "Coordinates and Movement",
        "topic_endpoint": "coordinates_topic",
        "difficulty": "Builder / Inventor",
        "estimated_time": "45-90 minutes",
        "topics": ["Coordinates", "Movement", "Random Positions", "Sensing", "Collision", "Variables", "Debugging"],
        "meta_description": (
            "Build Astro-Chicken Rescue, a Scratch Computer Lab project using "
            "multiple object coordinates, random positions, sensing, variables, and debugging."
        ),
        "mission": (
            "Several space chickens have drifted away from their station. Control the "
            "rescue ship, collect them, and avoid dangerous zones."
        ),
        "card_summary": (
            "Collect drifting space chickens while tracking several positions "
            "and avoiding danger zones."
        ),
        "lab_note": (
            "This project changes the coordinate lesson by making every rescue target a "
            "position problem. Students choose how chickens appear, how collection works, "
            "and how the ship receives useful information."
        ),
        "required_systems": [
            "A controllable rescue ship",
            "Several chickens at different or generated positions",
            "Collection detection",
            "One or more hazards",
            "A rescued-chicken counter",
            "A clear win condition",
        ],
        "build_order": [
            "Build and test ship movement from a known starting position.",
            "Place one chicken and make collection reliable.",
            "Add more chickens at distinct coordinates.",
            "Count rescues without counting the same chicken twice.",
            "Add a danger zone with clear collision behaviour.",
            "Create and test a win condition after all rescues are complete.",
        ],
        "checkpoints": [
            "The ship and every chicken have inspectable positions.",
            "Collecting one chicken changes the count once.",
            "Hazards and chickens cannot create contradictory outcomes.",
            "The win condition matches the number of rescue targets.",
            "The student can explain how an object's coordinates affected a test.",
        ],
        "challenge_cards": [
            "Randomize chicken locations.",
            "Make chickens drift slowly.",
            "Add limited oxygen.",
            "Require a rescue order based on coordinates.",
            "Define danger-zone boundaries using position.",
            "Add an optional two-player rescue mode.",
            "Create a radar display using relative position.",
        ],
        "boss_level": (
            "Create a rescue beacon that compares the ship and chicken positions and "
            "reports clues such as 'target is left and above.' This introduces relative "
            "position by comparing x values and y values without requiring formal vector mathematics."
        ),
        "demonstrate": [
            "Ship movement from a known start",
            "Several objects with different coordinates",
            "A successful rescue",
            "A working hazard",
            "A reliable win condition",
            "One independently chosen challenge card",
        ],
        "parent_explanation": (
            "This project extends coordinates from one player into a system of multiple "
            "moving or generated objects. Students work with random positions, sensing, "
            "collision, variables, planning, and debugging while keeping object states consistent."
        ),
    },
}
