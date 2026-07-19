from scratch_content import load_scratch_project


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


PROJECT_DETAILS["escape-from-the-giant-pigeon"].update(
    load_scratch_project("escape-from-the-giant-pigeon.json")
)


PROGRAM_LINKS = {
    "scratch": {"name": "Scratch & Game Design", "url": "/programs/scratch", "status": "Active now", "status_class": "active"},
    "robotics": {"name": "Robotics", "url": "/programs/robotics", "status": "Active now", "status_class": "active"},
    "roblox": {"name": "Roblox Studio / Lua", "url": "/programs/roblox", "status": "Available later", "status_class": "later"},
    "ai": {"name": "AI & Smart Machines", "url": "/programs/ai", "status": "Available later", "status_class": "later"},
}


def topic_entry(
    title,
    summary,
    status,
    programs,
    why_it_matters,
    logic_kernel,
    real_world_story,
    examples,
    common_mistakes,
    parent_note,
    lesson_slug,
    related_projects,
    related_topics,
):
    return {
        "title": title,
        "summary": summary,
        "intro": summary,
        "status": status,
        "status_class": "active" if status == "Complete topic package" else "demo",
        "programs": programs,
        "why_it_matters": why_it_matters,
        "logic_kernel": logic_kernel,
        "real_world_story": real_world_story,
        "examples": examples,
        "common_mistakes": common_mistakes,
        "parent_note": parent_note,
        "lesson_slug": lesson_slug,
        "related_projects": related_projects,
        "related_topics": related_topics,
    }


TOPICS.update(
    {
        "events-and-commands": topic_entry(
            "Events and Commands",
            "Programs need a reason to begin and a precise instruction about what should happen next. Events provide the reason; commands provide the action.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "Without events, a game cannot tell the difference between waiting and acting. "
                "Without commands, a robot has no sequence to follow. This topic gives students "
                "the basic grammar of interactive systems: when something happens, do something observable."
            ),
            [
                ("Trigger", "An event that starts a response."),
                ("Sequence", "Commands run in an intentional order."),
                ("Cause and effect", "A visible action should have an identifiable cause."),
                ("Specificity", "A useful command says exactly what changes."),
            ],
            (
                "An elevator button, a pedestrian crossing, and a game controller all wait for "
                "an event. The systems differ, but each must connect an input to a dependable sequence."
            ),
            [
                ("Green flag", "Start a Scratch scene from a known state."),
                ("Key press", "Move or act only when a chosen key is pressed."),
                ("Button input", "Make a simulated or physical output respond."),
                ("Message received", "Start one part of a project when another part is ready."),
            ],
            [
                ("Commands in the wrong order", "The output happens before the setup is complete."),
                ("No clear trigger", "Code exists but nothing tells it to run."),
                ("Too many jobs in one event", "A single script becomes difficult to test."),
                ("Assuming instant completion", "The next command begins before an animation or movement has finished."),
            ],
            (
                "A button-controlled animation looks simple, but it teaches children to connect "
                "cause and effect, order instructions, and explain why a system acted at a particular moment."
            ),
            "events-and-commands",
            ["robot-hamster-command-centre", "button-and-buzzer-alarm", "quiz-of-questionable-knowledge"],
            ["loops-and-repetition", "input-and-output", "debugging"],
        ),
        "loops-and-repetition": topic_entry(
            "Loops and Repetition",
            "A loop asks a program to repeat useful work without copying the same instruction again and again.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "Games constantly redraw motion, check collisions, create waves, and update timers. "
                "Robots repeatedly read sensors and correct movement. Loops make that repetition visible, "
                "controllable, and easier to change."
            ),
            [
                ("Repeat count", "Do an action a known number of times."),
                ("Forever", "Continue while the program is running."),
                ("Repeat until", "Stop when a condition becomes true."),
                ("Iteration", "One pass through the repeated instructions."),
            ],
            (
                "A lighthouse repeats a pattern, a traffic signal cycles through states, and a patrol "
                "checks the same route. Repetition becomes useful when the system also knows when to change or stop."
            ),
            [
                ("Snowball wave", "Create repeated hazards with controlled timing."),
                ("Animation cycle", "Repeat costume and position changes."),
                ("Robot patrol", "Repeat movement while checking for an obstacle."),
                ("Countdown", "Update a value once per timed interval."),
            ],
            [
                ("Accidental forever loop", "The program never reaches the instructions after the loop."),
                ("No changing value", "A repeat-until condition can never become true."),
                ("Copying instead of looping", "Many identical blocks make one change tedious and error-prone."),
                ("Repeating too quickly", "The result is unreadable because timing was never considered."),
            ],
            (
                "Loops are not merely shortcuts. They help students describe patterns, reason about "
                "how often something happens, and decide what condition should end repeated behaviour."
            ),
            "loops-and-repetition",
            ["attack-of-the-angry-snowballs", "robot-patrol-challenge", "the-floor-is-definitely-lava"],
            ["conditions-and-decisions", "variables-and-state", "feedback"],
        ),
        "conditions-and-decisions": topic_entry(
            "Conditions and Decisions",
            "Conditions let a program choose between actions by asking a question that can be answered yes or no.",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "A game needs to decide whether a player won, a quiz needs to check an answer, and a robot "
                "needs to decide whether an obstacle is close enough to matter. Conditions turn information into behaviour."
            ),
            [
                ("Boolean question", "A test with a true or false result."),
                ("If", "Run an action only when a condition is true."),
                ("If / else", "Choose between two paths."),
                ("Comparison", "Test whether values are equal, greater, or less."),
            ],
            (
                "A thermostat asks whether a room is colder than its target. The important part is not "
                "the appliance; it is the boundary between two decisions and what happens on each side."
            ),
            [
                ("Quiz answer", "Compare a response with the expected value."),
                ("Safe zone", "Win if the player reaches a target."),
                ("Obstacle check", "Turn if a sensor reports something close."),
                ("Fuel warning", "Change behaviour below a chosen threshold."),
            ],
            [
                ("Checking once", "A changing game condition is tested only at startup."),
                ("Reversed comparison", "The warning appears above the threshold instead of below it."),
                ("Overlapping outcomes", "Win and loss can both become true without a priority rule."),
                ("Hidden assumption", "The code assumes a value or state that was never initialized."),
            ],
            (
                "Conditions teach students to turn vague rules into testable questions. Parents can ask, "
                "'What question is the program asking, and what happens for each answer?'"
            ),
            "conditions-and-decisions",
            ["quiz-of-questionable-knowledge", "escape-from-the-giant-pigeon", "robot-patrol-challenge"],
            ["sensing-and-collision", "variables-and-state", "autonomy"],
        ),
        "variables-and-state": topic_entry(
            "Variables and State",
            "Variables give names to information that can change. State describes which situation the whole system is currently in.",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "Scores, health, fuel, mood, timers, current questions, and robot modes all need memory. "
                "A named value lets students inspect that memory instead of hiding it inside a complicated script."
            ),
            [
                ("Name", "A useful variable name describes the information stored."),
                ("Initial value", "Every test should begin from a known value."),
                ("Update", "An event changes a value for a reason."),
                ("State", "A label such as PLAYING, CAUGHT, or DELIVERING controls the current rules."),
            ],
            (
                "A taxi meter remembers a fare while the vehicle moves. A game score and a robot patrol mode "
                "do the same kind of work: they preserve information so later decisions can use it."
            ),
            [
                ("Score", "Increase after a completed action, not every frame."),
                ("Pet mood", "Store a changing need and show its effect."),
                ("Game state", "Separate starting, playing, won, and lost behaviour."),
                ("Robot mode", "Remember whether a machine is waiting, moving, or correcting."),
            ],
            [
                ("Never resetting", "A new game begins with values from the previous run."),
                ("Changing in two places", "A score jumps unexpectedly because several scripts update it."),
                ("Vague names", "Variables called thing or number hide their purpose."),
                ("Confusing value and display", "Hiding a variable monitor does not reset its stored value."),
            ],
            (
                "Variables make invisible memory visible. A child who can explain why a score changed, "
                "where it resets, and which state is active is reasoning about a complete system."
            ),
            "variables-and-score",
            ["the-suspiciously-emotional-space-pet", "grandmas-intergalactic-taxi", "microbit-reaction-timer"],
            ["conditions-and-decisions", "loops-and-repetition", "debugging"],
        ),
        "sensing-and-collision": topic_entry(
            "Sensing and Collision",
            "Sensing gives a program information about contact, distance, colour, input, or another changing part of the world.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "Movement alone does not create interaction. Games become systems when they notice walls, hazards, "
                "targets, or players. Robots become responsive when they can measure something outside their command list."
            ),
            [
                ("Signal", "A piece of information the program can inspect."),
                ("Collision", "Two regions overlap or touch."),
                ("Boundary", "A position or region that changes the rules."),
                ("Continuous checking", "Changing inputs must often be tested repeatedly."),
            ],
            (
                "A door sensor, a phone screen, and a game hitbox all decide whether an interaction occurred. "
                "The measurements differ, but each must define what counts as contact."
            ),
            [
                ("Touching colour", "Treat a map colour as a wall or hazard."),
                ("Sprite collision", "Detect contact between player and target."),
                ("Distance reading", "Respond when an object is nearer than a threshold."),
                ("Button sensing", "Turn a physical action into a program signal."),
            ],
            [
                ("Oversized collision area", "Transparent or hidden parts of a costume trigger contact."),
                ("One-time check", "Fast movement passes through because collision is not checked continuously."),
                ("No response state", "Contact is detected repeatedly and score increases many times."),
                ("Visual guess", "The student assumes objects touch instead of inspecting the sensing result."),
            ],
            (
                "Collision projects teach children to define evidence. The question is not only 'Did it look close?' "
                "but 'What signal did the program test, and what rule followed?'"
            ),
            "sensing-and-collision",
            ["the-floor-is-definitely-lava", "astro-chicken-rescue", "button-and-buzzer-alarm"],
            ["coordinates", "conditions-and-decisions", "sensors"],
        ),
        "input-and-output": topic_entry(
            "Input and Output",
            "Input is information entering a system. Output is the visible, audible, or physical action the system produces.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "Naming inputs and outputs helps students stop treating devices as magic. A key press is input; "
                "a moving sprite is output. A button is input; an LED or buzzer is output. Code connects them."
            ),
            [
                ("Input", "A signal the program can read."),
                ("Processing", "Rules that decide how the signal matters."),
                ("Output", "An action people or other systems can observe."),
                ("Mapping", "The deliberate connection between input and response."),
            ],
            (
                "A doorbell maps a button press to sound. A keyboard-controlled game and a microcontroller circuit "
                "use the same input-process-output structure with different materials."
            ),
            [
                ("Keyboard to movement", "Map four keys to coordinate changes."),
                ("Button to buzzer", "Produce sound while or after a button is pressed."),
                ("Timer to display", "Show a measured result."),
                ("Sensor to motor", "Change movement after a measurement."),
            ],
            [
                ("Input never read", "The program defines an output but does not check the signal."),
                ("Output has no clear cause", "Several inputs control the same action without priority."),
                ("Wrong pin or object", "Code listens to a different input than the build uses."),
                ("No feedback", "The user cannot tell whether the input was recognized."),
            ],
            (
                "Input and output give parents a plain way to discuss a project: What information entered, "
                "what rule processed it, and what observable action came out?"
            ),
            "robot-commands-and-sequences",
            ["button-and-buzzer-alarm", "led-traffic-light", "robot-hamster-command-centre"],
            ["events-and-commands", "sensors", "feedback"],
        ),
        "debugging": topic_entry(
            "Debugging",
            "Debugging is the disciplined work of explaining the difference between what a system should do and what it actually does.",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "Every substantial project contains surprises. Debugging teaches students to slow down, preserve evidence, "
                "test one idea at a time, and treat a bug as a clue rather than a judgment about ability."
            ),
            [
                ("Expected result", "State what should happen before changing code."),
                ("Observed result", "Describe what actually happened without guessing why."),
                ("Hypothesis", "Choose one possible cause."),
                ("Controlled test", "Change or inspect one relevant thing."),
            ],
            (
                "Repairing a bicycle, tracing a circuit, and debugging a game all depend on separating symptoms "
                "from causes. Random changes can hide information; a controlled test creates it."
            ),
            [
                ("Show coordinates", "Inspect position when movement seems wrong."),
                ("Display state", "Reveal whether the game thinks it is playing or finished."),
                ("Reduce the system", "Test one sprite, sensor, or rule alone."),
                ("Reproduce the bug", "Find a repeatable sequence that causes the problem."),
            ],
            [
                ("Changing many things", "The project works again but nobody knows which change mattered."),
                ("Testing only success", "The easiest path works while boundaries remain broken."),
                ("Blaming the tool", "A precise program rule is overlooked because the result feels unreasonable."),
                ("Fixing the symptom", "Extra code covers the visible problem while the underlying state remains wrong."),
            ],
            (
                "Debugging develops patience without asking children merely to endure frustration. They learn a method: "
                "describe, inspect, predict, test, and explain."
            ),
            "debugging-clues",
            ["escape-from-the-giant-pigeon", "robot-maze-logic", "microbit-reaction-timer"],
            ["variables-and-state", "feedback", "conditions-and-decisions"],
        ),
        "sensors": topic_entry(
            "Sensors",
            "A sensor turns part of the physical world into information a program can inspect.",
            "Project connection",
            ["robotics", "ai"],
            (
                "Robots cannot respond intelligently without information. Sensors measure light, distance, motion, "
                "temperature, touch, sound, or other signals, but every reading has limits and noise."
            ),
            [
                ("Measurement", "A value representing part of the world."),
                ("Threshold", "A chosen boundary between responses."),
                ("Noise", "Small changes or errors in readings."),
                ("Sampling", "Reading a changing signal repeatedly over time."),
            ],
            (
                "Automatic lights do not see darkness as a person does. They receive a number from a light sensor "
                "and compare it with a threshold chosen by a designer."
            ),
            [
                ("Button", "A simple two-state sensor: pressed or not pressed."),
                ("Distance", "Estimate how near an obstacle is."),
                ("Light level", "Change output when a space becomes darker."),
                ("Accelerometer", "Measure movement or orientation on a microcontroller."),
            ],
            [
                ("Treating readings as perfect", "A system reacts badly to small fluctuations."),
                ("Poor threshold", "The decision boundary does not match the actual environment."),
                ("No calibration", "The program assumes every room or device produces the same values."),
                ("Confusing sensor and decision", "The sensor measures; the code decides what the measurement means."),
            ],
            (
                "Sensor work teaches that data does not explain itself. Students must ask what was measured, "
                "how reliable it is, and what rule should follow."
            ),
            "sensors-as-questions",
            ["button-and-buzzer-alarm", "microbit-reaction-timer", "robot-patrol-challenge"],
            ["input-and-output", "feedback", "autonomy"],
        ),
        "feedback": topic_entry(
            "Feedback",
            "Feedback happens when a system checks the result of an action and uses that information to adjust what it does next.",
            "Project connection",
            ["robotics", "scratch", "ai"],
            (
                "A command can start movement, but feedback makes movement correctable. Games use score and collision signals; "
                "robots use sensor readings; people use visible results to improve a design."
            ),
            [
                ("Goal", "The result the system is trying to maintain or reach."),
                ("Observation", "Information about the current result."),
                ("Difference", "How current behaviour differs from the goal."),
                ("Correction", "A change intended to reduce that difference."),
            ],
            (
                "A person steering a bicycle makes many small corrections after seeing where the bicycle goes. "
                "A robot patrol can do something similar with repeated sensing and turning."
            ),
            [
                ("Boundary correction", "Move a sprite back when it leaves a region."),
                ("Line following", "Adjust direction after reading a surface."),
                ("Speed tuning", "Change movement after measuring timing."),
                ("Player feedback", "Use sound or display to make a system state visible."),
            ],
            [
                ("Correction without measurement", "The system changes repeatedly without checking whether it helped."),
                ("Correction too large", "The result swings past the goal."),
                ("Feedback too late", "The system reacts after the useful moment has passed."),
                ("Hidden goal", "Students cannot explain what the system is trying to maintain."),
            ],
            (
                "Feedback connects action with evidence. A student learns that improvement is not a guess: "
                "observe the result, compare it with the goal, and make a measured correction."
            ),
            "robot-patrol-logic",
            ["robot-patrol-challenge", "microbit-reaction-timer", "the-floor-is-definitely-lava"],
            ["sensors", "loops-and-repetition", "autonomy"],
        ),
        "autonomy": topic_entry(
            "Autonomy",
            "An autonomous system uses information and rules to act without a person choosing every individual command.",
            "Available later connection",
            ["robotics", "ai"],
            (
                "Autonomy combines earlier ideas: sensing, conditions, loops, state, feedback, goals, and careful testing. "
                "It is not a single magic feature and it does not mean a machine understands the world like a person."
            ),
            [
                ("Goal", "A defined result the system attempts to reach."),
                ("Policy", "Rules connecting observations to actions."),
                ("State", "Information retained between decisions."),
                ("Human boundary", "Limits and decisions that remain a person's responsibility."),
            ],
            (
                "A basic robot vacuum can choose movement from sensor readings, yet it still has limited goals, "
                "limited knowledge, and rules designed by people. Autonomy should always be described with those limits."
            ),
            [
                ("Patrol rule", "Choose a turn after detecting an obstacle."),
                ("Game opponent", "Select a simple action from player distance and current state."),
                ("Recovery behaviour", "Return to a safe state after an error."),
                ("Stop condition", "End autonomous action when a boundary is reached."),
            ],
            [
                ("Calling any movement autonomous", "A fixed sequence does not respond to changing information."),
                ("No stop rule", "The system continues when a person expects it to stop."),
                ("Overstating intelligence", "Successful rules are described as understanding."),
                ("Ignoring edge cases", "The system works only in the exact test arrangement."),
            ],
            (
                "Autonomy is a later synthesis topic. Students first need dependable experience with commands, "
                "sensors, decisions, state, and feedback before combining them into more independent behaviour."
            ),
            "robot-patrol-logic",
            ["robot-patrol-challenge", "ai-guessing-game"],
            ["sensors", "feedback", "conditions-and-decisions"],
        ),
    }
)


TOPICS["coordinates"].update(
    {
        "summary": TOPICS["coordinates"]["intro"],
        "status": "Complete topic package",
        "status_class": "active",
        "programs": ["scratch", "robotics", "roblox", "ai"],
        "why_it_matters": (
            "Coordinates connect number lines to visible movement. They let students predict where an object will go, "
            "define boundaries, compare positions, and debug a map instead of moving sprites by guesswork."
        ),
        "logic_kernel": TOPICS["coordinates"]["math_kernel"],
        "real_world_story": (
            "Maps, screen layouts, robot navigation, drones, and computer vision all need a representation of position. "
            "This first topic does not teach those advanced systems; it establishes the idea that returns inside them."
        ),
        "examples": [
            ("Known start", "Place a player at x: -180, y: -100 for every test."),
            ("Horizontal movement", "Change x while keeping y unchanged."),
            ("Vertical movement", "Change y while keeping x unchanged."),
            ("Relative clue", "Compare two positions to decide left/right and above/below."),
        ],
        "lesson_slug": "coordinates-and-movement",
        "related_projects": ["escape-from-the-giant-pigeon", "grandmas-intergalactic-taxi", "astro-chicken-rescue"],
        "related_topics": ["sensing-and-collision", "variables-and-state", "debugging"],
    }
)


def lesson_entry(
    title,
    program_key,
    topic_slug,
    story,
    learning_goals,
    theory_examples,
    guided_project,
    checkpoints,
    common_mistakes,
    challenges,
    demonstration_questions,
    parent_summary,
):
    return {
        "title": title,
        "program_key": program_key,
        "program": PROGRAM_LINKS[program_key]["name"],
        "topic_slug": topic_slug,
        "topic": TOPICS[topic_slug]["title"],
        "duration": "90 minutes",
        "age_language": "Beginner-friendly; challenge depth can be adjusted for the group.",
        "story": story,
        "learning_goals": learning_goals,
        "theory_examples": theory_examples,
        "guided_project": guided_project,
        "checkpoints": checkpoints,
        "common_mistakes": common_mistakes,
        "challenge_levels": challenges,
        "demonstration_questions": demonstration_questions,
        "parent_summary": parent_summary,
    }


STANDARD_TIMELINE = [
    ("0-10 min", "Story, problem, or provocation", "Name the problem before opening the build."),
    ("10-30 min", "Theory and concept", "Make the hidden rule visible with small tests."),
    ("30-65 min", "Guided build", "Use the idea inside a working project system."),
    ("65-80 min", "Modification challenge", "Change one rule and predict the effect."),
    ("80-90 min", "Demonstration and cleanup", "Explain the result, save safely, and leave a known state."),
]


LESSONS.update(
    {
        "events-and-commands": lesson_entry(
            "What Makes a Program Start?",
            "scratch",
            "events-and-commands",
            "A robot hamster receives five commands, but nobody tells it when to begin. Is the command list broken, or is the missing event the real problem?",
            ["Identify an event and its response.", "Order commands intentionally.", "Predict a short sequence before running it.", "Separate setup from repeated behaviour.", "Explain one cause-and-effect link."],
            [("when green flag clicked", "begin from a known state"), ("when space key pressed", "respond to one input"), ("broadcast START", "signal another script"), ("move / turn / wait", "create an ordered sequence")],
            "robot-hamster-command-centre",
            ["Student names the trigger.", "Student predicts a three-command sequence.", "Restart produces the same setup.", "One event has one clear responsibility.", "Student changes the order and explains the result."],
            ["Code has no trigger.", "Setup runs after movement.", "Two events fight over the same output.", "The student changes timing without testing sequence order."],
            [{"name": "Builder", "ideas": ["Add a second command key."]}, {"name": "Inventor", "ideas": ["Broadcast a mission-complete event."]}, {"name": "Boss Level", "ideas": ["Build a queue of commands before execution."]}],
            ["What event starts the program?", "Which command runs first?", "What changed when the order changed?", "Which part is setup?", "What did you debug?"],
            "Students practised the grammar of interactive programs: an event starts a response, commands run in an intentional order, and changing that order changes the visible result.",
        ),
        "loops-and-repetition": lesson_entry(
            "How Many Times Should the Snowballs Attack?",
            "scratch",
            "loops-and-repetition",
            "A snowball attack works once. Copying it fifty times works too, but nobody wants to repair fifty copies when the timing changes. What should repeat, and what should stop it?",
            ["Recognize repeated instructions.", "Choose repeat, forever, or repeat-until.", "Count iterations.", "Change timing inside a loop.", "Explain a stop condition."],
            [("repeat 10", "run a known number of waves"), ("forever", "keep checking while the game runs"), ("repeat until score = 8", "stop after a goal"), ("wait 0.5 seconds", "make repetition observable")],
            "attack-of-the-angry-snowballs",
            ["Student replaces copied blocks with a loop.", "Student predicts the repeat count.", "The loop contains a changing action.", "The game has a stop or state rule.", "Student tunes timing independently."],
            ["A forever loop blocks later code.", "Repeat-until never changes its condition.", "The loop creates objects too quickly.", "Setup accidentally repeats with every wave."],
            [{"name": "Builder", "ideas": ["Add a fixed second wave."]}, {"name": "Inventor", "ideas": ["Shorten the delay as score rises."]}, {"name": "Boss Level", "ideas": ["Create wave states with different patterns."]}],
            ["What repeats?", "How many times?", "What changes each time?", "What stops the loop?", "Which repeated copy did you remove?"],
            "Students used loops to describe repeated game behaviour, selected a stopping rule, and tested how timing and changing values affect each iteration.",
        ),
        "conditions-and-decisions": lesson_entry(
            "How Does a Game Decide?",
            "scratch",
            "conditions-and-decisions",
            "The Quiz of Questionable Knowledge accepts 'moon cheese' as an answer. Should it celebrate, object politely, or ask another question? The program needs rules it can actually test.",
            ["Turn a rule into a true/false question.", "Use if and if/else.", "Compare values.", "Order overlapping decisions.", "Explain why one branch ran."],
            [("if answer = 'Ottawa'", "test equality"), ("if score > 5", "test a threshold"), ("if touching danger", "use sensing in a decision"), ("else", "define the other path")],
            "quiz-of-questionable-knowledge",
            ["Student states the question in words.", "Both true and false paths can be demonstrated.", "The comparison uses the intended value.", "Only one answer scores each question.", "Student adds one independent decision."],
            ["Using assignment language instead of comparison.", "Checking a changing condition only once.", "Two branches score the same answer.", "An else belongs to the wrong if."],
            [{"name": "Builder", "ideas": ["Add feedback for a wrong answer."]}, {"name": "Inventor", "ideas": ["Accept two equivalent spellings."]}, {"name": "Boss Level", "ideas": ["Choose question difficulty from score."]}],
            ["What question does the code ask?", "What makes it true?", "What happens otherwise?", "Can two outcomes happen together?", "What rule did you add?"],
            "Students turned game rules into testable conditions, compared values, and explained why the program selected one branch rather than another.",
        ),
        "variables-and-score": lesson_entry(
            "Where Does the Score Live?",
            "scratch",
            "variables-and-state",
            "A space pet insists it was fed, but the program has forgotten. What information must the game remember, when should it change, and when should a new run reset it?",
            ["Create a meaningfully named variable.", "Set an initial value.", "Update a value from an event.", "Use a value in a condition.", "Separate score, state, and visual display."],
            [("set mood to 5", "initialize memory"), ("change mood by -1", "update over time"), ("if mood < 2", "make a decision from memory"), ("set game_state to PLAYING", "name the current mode")],
            "the-suspiciously-emotional-space-pet",
            ["Variable name describes its purpose.", "Restart restores the initial value.", "One event changes the value once.", "A condition reads the value.", "Student explains the current state."],
            ["Variable never resets.", "Several scripts change the score unexpectedly.", "A display is hidden but the value remains.", "Text and number values are compared accidentally."],
            [{"name": "Builder", "ideas": ["Add a second need such as energy."]}, {"name": "Inventor", "ideas": ["Make needs affect each other."]}, {"name": "Boss Level", "ideas": ["Create named pet states from several variables."]}],
            ["What does the variable remember?", "Where is it initialized?", "Which event changes it?", "Which decision reads it?", "What state is active now?"],
            "Students used variables as visible memory, initialized values, updated them for specific reasons, and connected changing values to decisions and game state.",
        ),
        "sensing-and-collision": lesson_entry(
            "How Does the Game Know You Touched the Lava?",
            "scratch",
            "sensing-and-collision",
            "The floor looks extremely lava-like, but the computer does not care about appearances. What exactly counts as touching danger, and how often should the game check?",
            ["Identify a sensing signal.", "Define a collision or boundary.", "Check a changing signal repeatedly.", "Prevent repeated scoring from one contact.", "Inspect collision evidence while debugging."],
            [("touching Lava?", "test sprite contact"), ("touching colour red?", "test a map region"), ("distance to hazard < 40", "test nearness"), ("if touching then set state", "turn sensing into behaviour")],
            "the-floor-is-definitely-lava",
            ["Student can show the collision area.", "Sensing is checked while movement occurs.", "One contact causes one state change.", "Restart clears the collision state.", "Student tests a fast boundary crossing."],
            ["Costume transparency makes the hitbox surprising.", "Contact is checked only at startup.", "Score rises every frame during one collision.", "A visual overlap is assumed without reading the sensing result."],
            [{"name": "Builder", "ideas": ["Add one safe platform."]}, {"name": "Inventor", "ideas": ["Make platforms move while preserving collision."]}, {"name": "Boss Level", "ideas": ["Create one-way or temporary safe surfaces."]}],
            ["What signal counts as contact?", "How often is it checked?", "What state changes?", "How did you test the boundary?", "What collision bug did you fix?"],
            "Students defined collision evidence, repeatedly checked changing inputs, and used conditions and state to turn contact into reliable game behaviour.",
        ),
        "debugging-clues": lesson_entry(
            "What Is the Bug Trying to Tell You?",
            "scratch",
            "debugging",
            "The game works unless the player wins while being caught near the right edge. Random repairs make it stranger. Can we reproduce the bug and make one useful test?",
            ["Separate expected and observed results.", "Reproduce a bug.", "Inspect visible values or state.", "Form one hypothesis.", "Run a controlled test and explain the evidence."],
            [("show x position", "inspect movement evidence"), ("say game_state", "reveal hidden mode"), ("disable one script", "reduce the system"), ("repeat the same inputs", "test reproducibility")],
            "escape-from-the-giant-pigeon",
            ["Student describes the bug without guessing.", "A repeatable sequence triggers it.", "One relevant value is inspected.", "One hypothesis is tested at a time.", "The repair is explained with evidence."],
            ["Changing several scripts at once.", "Testing only the successful path.", "Adding delays to hide a state problem.", "Stopping after the symptom disappears once."],
            [{"name": "Builder", "ideas": ["Create a bug report with exact steps."]}, {"name": "Inventor", "ideas": ["Add temporary on-screen state monitors."]}, {"name": "Boss Level", "ideas": ["Design an automated edge-case test sequence."]}],
            ["What should happen?", "What actually happens?", "How can you reproduce it?", "What evidence did you inspect?", "Why did the fix work?"],
            "Students treated a bug as information: they reproduced it, inspected relevant state, tested one possible cause, and explained the repair using evidence.",
        ),
        "robot-commands-and-sequences": lesson_entry(
            "Can a Robot Follow Your Instructions?",
            "robotics",
            "input-and-output",
            "A delivery robot receives 'go around the chair' as one command. A person understands; the robot does not. How can we replace vague intent with a sequence that can be tested on paper or in simulation?",
            ["Break a goal into commands.", "Order movement and turn instructions.", "Predict final position and direction.", "Test a sequence in simulation or on paper.", "Revise one incorrect command."],
            [("forward 2", "move a measured amount"), ("turn right", "change direction, not position"), ("pause", "separate actions visibly"), ("repeat route", "reuse a reliable sequence")],
            "robot-maze-logic",
            ["Each command has one meaning.", "Student predicts before running.", "Direction is tracked after each turn.", "The route reaches the target.", "One revision is justified."],
            ["Using human phrases the system cannot execute.", "Losing track of direction after turns.", "Changing several route steps after one failure.", "Assuming the robot occupies no space."],
            [{"name": "Builder", "ideas": ["Add one obstacle and reroute."]}, {"name": "Inventor", "ideas": ["Create reusable route segments."]}, {"name": "Boss Level", "ideas": ["Write a route checker for a grid map."]}],
            ["What is the goal?", "Which command runs first?", "Where does the robot face now?", "Which command failed?", "How did the revision change the route?"],
            "Students translated a human goal into precise commands, tracked movement and direction, predicted a sequence, and revised one instruction from test evidence. Hardware was not required for the reasoning.",
        ),
        "sensors-as-questions": lesson_entry(
            "What Question Is the Sensor Answering?",
            "robotics",
            "sensors",
            "A machine reports 347. Is that bright, close, tilted, pressed, or meaningless? A sensor reading becomes useful only when we know what was measured and how the program interprets it.",
            ["Identify what a sensor measures.", "Read a changing value.", "Choose and test a threshold.", "Distinguish measurement from decision.", "Explain noise or variation."],
            [("button = pressed", "read a two-state input"), ("distance < 15", "compare a measurement with a threshold"), ("light level", "inspect a changing value"), ("read repeatedly", "sample over time")],
            "microbit-reaction-timer",
            ["Student names the measured quantity.", "Several readings are observed.", "A threshold is stated and tested.", "Output changes for a clear reason.", "Student identifies one limitation."],
            ["Treating readings as perfect.", "Choosing a threshold from one test only.", "Calling the sensor intelligent.", "Changing output without recording the input value."],
            [{"name": "Builder", "ideas": ["Display raw readings before deciding."]}, {"name": "Inventor", "ideas": ["Compare two candidate thresholds."]}, {"name": "Boss Level", "ideas": ["Smooth several readings before acting."]}],
            ["What does the sensor measure?", "What values did you observe?", "Where is the threshold?", "What does the code decide?", "When could the reading be wrong?"],
            "Students treated sensors as measurement tools rather than magic. They observed changing values, selected a threshold, separated sensing from decision-making, and discussed limits in the data.",
        ),
        "robot-patrol-logic": lesson_entry(
            "How Can a Robot Patrol Without Getting Stuck?",
            "robotics",
            "feedback",
            "A patrol robot follows its route perfectly until somebody moves a box. Should it continue, stop forever, or use a sensor reading to choose a recovery action?",
            ["Combine a repeated patrol with sensing.", "Use a condition to choose a correction.", "Represent patrol state.", "Test an obstacle edge case.", "Explain the feedback loop."],
            [("repeat patrol", "continue the route"), ("if obstacle near", "detect a reason to change"), ("turn and check again", "correct from new information"), ("state = RECOVERING", "remember the current mode")],
            "robot-patrol-challenge",
            ["A normal patrol can be demonstrated.", "An obstacle changes behaviour.", "The system checks again after correcting.", "Recovery does not become an endless turn.", "Student explains Sense-Decide-Act."],
            ["Patrol never reads the sensor.", "One obstacle causes permanent recovery mode.", "Turning occurs without checking the result.", "The stop condition is missing."],
            [{"name": "Builder", "ideas": ["Stop and signal at an obstacle."]}, {"name": "Inventor", "ideas": ["Try a second route after turning."]}, {"name": "Boss Level", "ideas": ["Track failed directions and choose a recovery state."]}],
            ["What repeats during patrol?", "What does the system sense?", "Which condition changes the plan?", "How does it check the correction?", "What limit remains?"],
            "Students combined loops, sensing, conditions, and state into a simple feedback system. They tested how a patrol responds when the world differs from its original plan.",
        ),
    }
)


LESSONS["coordinates-and-movement"].update(
    {
        "program_key": "scratch",
        "topic_slug": "coordinates",
        "guided_project": "escape-from-the-giant-pigeon",
        "common_mistakes": [
            "Changing x when the intended movement is vertical.",
            "Using the wrong positive or negative sign.",
            "Testing from an unknown starting position.",
            "Confusing the direction a sprite faces with its position.",
        ],
    }
)


for lesson_slug, lesson in LESSONS.items():
    lesson.setdefault("timeline", STANDARD_TIMELINE)
    lesson["slug"] = lesson_slug
    lesson["url"] = f"/lessons/{lesson_slug}"
    punctuation = "" if lesson["title"].endswith((".", "?", "!")) else "."
    lesson.setdefault(
        "meta_description",
        f"School of Code lesson: {lesson['title']}{punctuation} A practical 90-minute public lesson for {lesson['program']}.",
    )

for topic_slug, topic in TOPICS.items():
    topic["slug"] = topic_slug
    topic["url"] = f"/topics/{topic_slug}"
    topic.setdefault("meta_description", f"School of Code topic guide: {topic['title']}, with plain explanations, examples, mistakes, projects, and parent notes.")


TOPIC_ORDER = [
    "events-and-commands",
    "coordinates",
    "loops-and-repetition",
    "conditions-and-decisions",
    "variables-and-state",
    "sensing-and-collision",
    "input-and-output",
    "debugging",
    "sensors",
    "feedback",
    "autonomy",
]

LESSON_ORDER = [
    "events-and-commands",
    "coordinates-and-movement",
    "loops-and-repetition",
    "conditions-and-decisions",
    "variables-and-score",
    "sensing-and-collision",
    "debugging-clues",
    "robot-commands-and-sequences",
    "sensors-as-questions",
    "robot-patrol-logic",
]
