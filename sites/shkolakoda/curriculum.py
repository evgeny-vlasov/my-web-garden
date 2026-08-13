from scratch_content import load_scratch_project


TOPICS = {
    "coordinates": {
        "title": "Coordinates and Movement",
        "endpoint": "coordinates_topic",
        "program": "Scratch & Game Design",
        "program_endpoint": "scratch",
        "intro": (
            "Coordinates give every place on the screen an address. Change x to move "
            "left or right; change y to move down or up."
        ),
        "meta_description": (
            "How x and y coordinates control position and movement in Scratch, maps, "
            "animation, robotics, and computer vision."
        ),
        "math_kernel": [
            ("Two number lines", "One runs horizontally and the other vertically."),
            ("Positive and negative", "The sign places a point on one side of the origin or the other."),
            ("x and y", "x controls left and right; y controls down and up."),
            ("Change in position", "Subtract the starting value from the finishing value to find the change."),
            ("The origin", "x: 0, y: 0 is the shared reference point at the centre of the stage."),
        ],
        "common_mistakes": [
            ("Changing the wrong axis", "The character moves sideways when it was meant to move vertically."),
            ("Using the wrong sign", "The sprite heads left when the student predicted right."),
            ("Forgetting to reset", "The same test gives a different result because the sprite starts somewhere new."),
            ("Ignoring the edge", "A loop keeps changing position after the sprite reaches the stage boundary."),
            ("Mixing up direction and position", "Where a sprite faces and where it stands are separate properties."),
            ("Adding blocks at random", "The useful clues are the sprite's current x and y values."),
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
            "Ask your child to predict the player's next coordinates before pressing a key. "
            "If the pigeon walks through a wall, ask which position or boundary rule needs checking."
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
        "age_language": "No previous Scratch experience is needed. Challenges can be extended for experienced students.",
        "meta_description": (
            "A 90-minute Scratch lesson on x and y coordinates, movement, boundaries, "
            "and debugging position."
        ),
        "story": (
            "A giant pigeon is chasing your character across Calgary. Give both sprites "
            "reliable positions, move the player with x and y, and decide exactly what "
            "counts as being caught."
        ),
        "timeline": [
            ("0-10 min", "The chase", "Work out how the stage records the player and pigeon positions."),
            ("10-30 min", "Coordinates", "Read x and y, predict changes, and return to the origin."),
            ("30-65 min", "Build the game", "Add movement, pursuit, collision, and a safe zone."),
            ("65-80 min", "Change a rule", "Choose one modification, predict the result, and try it."),
            ("80-90 min", "Show and explain", "Run the game and use coordinates to explain one part."),
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
            "The student can identify the origin.",
            "Four coordinate changes are predicted before they run.",
            "Restarting returns the player to the chosen position.",
            "The student explains one movement bug using x or y.",
            "At least one rule has been changed independently.",
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
            "Students used x and y coordinates to move a player, set reliable starting positions, "
            "and check the edge of the stage. They also used the coordinate display to explain "
            "and repair a movement bug in the pigeon chase game."
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
            "Build a Scratch chase game with coordinate movement, collision rules, "
            "game state, complete resets, and a very large pigeon."
        ),
        "mission": (
            "Reach the shelter before a huge pigeon catches you. Under the absurd premise "
            "is a precise system of coordinates, collision checks, and two possible endings."
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
            "This project runs in the browser-based Scratch editor, so there is nothing to install. "
            "An account is optional; available saving and sharing methods depend on the classroom setup."
        ),
        "build_steps": [
            {
                "title": "Create the player",
                "task": "Choose or draw a character that is easy to see against the map.",
                "explanation": "The arrow keys will change this sprite's position.",
                "checkpoint": "The player is visible and selected in the editor.",
                "mistake": "Editing the stage or pigeon when you meant to edit the player.",
            },
            {
                "title": "Set a known start",
                "task": "Choose a starting x and y position, then send the player there when the project begins.",
                "explanation": "Every test should begin from the same position.",
                "checkpoint": "Restarting always returns the player to the same place.",
                "mistake": "Moving the sprite by hand but never putting the starting position in code.",
            },
            {
                "title": "Add four-direction controls",
                "task": "Use keys to change x for left/right and y for down/up.",
                "explanation": "Right and left change x. Up and down change y.",
                "checkpoint": "Each key changes only the intended axis.",
                "mistake": "Changing y for a left/right key or using the wrong sign.",
            },
            {
                "title": "Add the giant pigeon",
                "task": "Draw or choose a bird-like sprite and give it a fixed starting point.",
                "explanation": "The pigeon needs coordinates of its own.",
                "checkpoint": "The pigeon never starts directly on top of the player.",
                "mistake": "Leaving its starting position wherever the previous test ended.",
            },
            {
                "title": "Make the pigeon pursue",
                "task": "Use a simple pursuit rule to make the pigeon keep moving toward the player.",
                "explanation": "The pigeon checks the player's latest position before each move.",
                "checkpoint": "The pigeon follows after the player moves.",
                "mistake": "Running the pursuit once instead of repeatedly.",
            },
            {
                "title": "Create a safe zone",
                "task": "Draw a clear destination and place it away from both starting positions.",
                "explanation": "The destination gives the player somewhere specific to reach.",
                "checkpoint": "The player can reach it with the keyboard controls.",
                "mistake": "Placing it partly outside the stage or beneath another object.",
            },
            {
                "title": "Detect being caught",
                "task": "Repeatedly check whether the player touches the pigeon.",
                "explanation": "Contact with the pigeon changes the game state to CAUGHT.",
                "checkpoint": "Touching the pigeon produces a clear loss state.",
                "mistake": "Checking collision before play begins but never checking again.",
            },
            {
                "title": "Detect reaching safety",
                "task": "Check whether the player touches the safe zone and switch to a win state.",
                "explanation": "Touching the safe zone produces the other ending.",
                "checkpoint": "Reaching safety ends the chase visibly.",
                "mistake": "Allowing win and loss to trigger during the same moment without deciding priority.",
            },
            {
                "title": "Reset the whole game",
                "task": "Return positions, messages, and game state to their initial values.",
                "explanation": "A restart restores both sprites, every variable, and the opening state.",
                "checkpoint": "Three restarts in a row behave the same way.",
                "mistake": "Resetting one sprite while the other keeps its old state.",
            },
            {
                "title": "Test strange situations",
                "task": "Try the stage edges, rapid keys, simultaneous contact, and unusual starting arrangements.",
                "explanation": "These tests reach cases that an ordinary successful run may miss.",
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
            "Students move the player by changing x and y, then use contact checks and game state "
            "to keep the two endings separate. A complete reset makes repeated testing possible. "
            "The pigeon is absurd. The coordinate system is not."
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
            "Build Grandma's Intergalactic Taxi in Scratch with coordinate routes, "
            "pickup and delivery states, boundaries, and a trip counter."
        ),
        "mission": (
            "Grandma drives a taxi in space and has no intention of missing another pickup. "
            "Read the map, collect passengers, and deliver them to the right coordinates."
        ),
        "card_summary": (
            "Navigate a space taxi between coordinate-based pickups and destinations."
        ),
        "lab_note": (
            "The required systems set the finish line. Students choose the map and controls, "
            "then decide how the taxi detects arrivals and handles dispatches."
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
            "Draw the map and write down the coordinates of each destination.",
            "Give the taxi a fixed starting position and add movement controls.",
            "Make arrival work at one station, then add the others.",
            "Create separate pickup and delivery states for one passenger.",
            "Count a completed trip once, then reset the current request.",
            "Try the map boundaries, wrong destinations, and repeated arrivals.",
        ],
        "checkpoints": [
            "The taxi always starts from the chosen coordinates.",
            "At least three destinations have distinct locations.",
            "Pickup and delivery are different states.",
            "One delivery adds exactly one trip.",
            "The student can explain one route using x and y changes.",
        ],
        "test_questions": [
            "Does the taxi always start at the chosen coordinates?",
            "Can it arrive at all three destinations?",
            "Can a passenger be delivered before being collected?",
            "Does one delivery add exactly one trip?",
            "What happens after a wrong destination or route?",
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
            "Make the dispatcher give coordinates instead of flashing the destination: "
            "'Pickup requested near x: 140, y: -80.' The player must read the request and navigate there."
        ),
        "demonstrate": [
            "Three destinations on a coordinate map",
            "A complete pickup and delivery",
            "A trip counter that changes once per delivery",
            "Recovery from a wrong route or mistake",
            "One independently chosen challenge card",
        ],
        "parent_explanation": (
            "Students use coordinates as places on a working map. The taxi must distinguish pickup "
            "from delivery, count each trip once, and recover from wrong destinations or bad routes. "
            "There may be several good routes, which makes comparison part of the project."
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
            "Build Astro-Chicken Rescue in Scratch with several coordinate positions, "
            "collision sensing, hazards, variables, and optional random targets."
        ),
        "mission": (
            "Several space chickens have drifted away from their station. Control the "
            "rescue ship, collect them, and avoid dangerous zones."
        ),
        "card_summary": (
            "Track several drifting chickens, collect them once each, and stay out of the danger zones."
        ),
        "lab_note": (
            "Every chicken adds another position for the game to track. Students decide where the targets "
            "appear, what counts as a rescue, and how much navigational help the ship provides."
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
            "Give the ship a fixed starting position, then build and test its controls.",
            "Place one chicken and make its collection rule reliable.",
            "Add more chickens at different coordinates.",
            "Make sure each chicken can increase the rescue count only once.",
            "Add a danger zone and define what its collision does.",
            "End the game when the rescue count matches the number of chickens.",
        ],
        "checkpoints": [
            "The positions of the ship and every chicken can be inspected.",
            "Collecting one chicken adds exactly one to the count.",
            "Touching a hazard and a chicken cannot produce contradictory outcomes.",
            "The win condition matches the number of rescue targets.",
            "The student uses an object's coordinates to explain one test result.",
        ],
        "test_questions": [
            "Can the ship and every chicken's position be inspected?",
            "Does collecting one chicken add exactly one to the count?",
            "What happens when the ship touches a hazard and a chicken together?",
            "Does the win condition match the number of rescue targets?",
            "Do all targets and counters reset for a new attempt?",
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
            "Create a beacon that compares the ship and chicken coordinates, then reports clues such as "
            "'target is left and above.' Compare the two x values and the two y values separately."
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
            "The game tracks a ship, several chickens, and at least one hazard at the same time. "
            "Students use collision sensing and a rescue counter, prevent the same target from scoring twice, "
            "and keep the win and hazard rules from contradicting each other."
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
            "An event tells a program when to respond. Commands say what to do, and their order matters.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "The green flag, a key press, and a robot's button are all triggers. Students connect "
                "each trigger to a short sequence, then change the order and watch the result change."
            ),
            [
                ("Trigger", "The event that starts a script."),
                ("Sequence", "The order in which commands run."),
                ("Cause and effect", "A key is pressed, so the sprite jumps."),
                ("Specific commands", "The program needs an action it can actually carry out."),
            ],
            (
                "Press an elevator button and a sequence begins: record the request, move the car, "
                "stop at the right floor, and open the door. Games and robots arrange their responses the same way."
            ),
            [
                ("Green flag", "Put a Scratch scene into its starting state."),
                ("Key press", "Run an action when the player chooses a key."),
                ("Button input", "Connect a physical press to a light or sound."),
                ("Message received", "Begin one script when another has finished its job."),
            ],
            [
                ("Wrong order", "The character moves before its position has been reset."),
                ("Missing trigger", "The blocks are correct, but nothing starts them."),
                ("One event doing everything", "A long script makes it hard to find which response failed."),
                ("Timing assumed", "The next command runs before a movement or animation has finished."),
            ],
            (
                "A student should be able to point to the event, name the first command, and predict what "
                "will change if two commands swap places."
            ),
            "events-and-commands",
            ["robot-hamster-command-centre", "button-and-buzzer-alarm", "quiz-of-questionable-knowledge"],
            ["loops-and-repetition", "input-and-output", "debugging"],
        ),
        "loops-and-repetition": topic_entry(
            "Loops and Repetition",
            "Loops repeat a group of commands. The programmer chooses what repeats, how often, and when it stops.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "A game checks for collisions many times each second. A robot keeps reading its distance sensor. "
                "Putting that work in a loop makes the repeated rule easy to see and change."
            ),
            [
                ("Repeat count", "Run the commands a fixed number of times."),
                ("Forever", "Keep running them while the project is active."),
                ("Repeat until", "Check a condition and stop when it becomes true."),
                ("Iteration", "One trip through the loop."),
            ],
            (
                "A traffic signal repeats a cycle, but it cannot simply flash every light at once. "
                "The sequence, timing, and stopping rule are part of the loop."
            ),
            [
                ("Snowball wave", "Launch each hazard after a controlled delay."),
                ("Animation cycle", "Repeat costume changes at a readable speed."),
                ("Robot patrol", "Move along the route and check for obstacles each time."),
                ("Countdown", "Subtract one after each timed interval."),
            ],
            [
                ("Accidental forever loop", "The program never reaches the blocks beneath it."),
                ("A condition that never changes", "The repeat-until loop has no way to finish."),
                ("Copied blocks", "One timing change has to be repaired in twenty places."),
                ("No pause", "The loop runs so quickly that the result cannot be seen or controlled."),
            ],
            (
                "The useful questions are simple: what belongs inside the loop, what happens only once, "
                "and which count or condition brings the repetition to an end?"
            ),
            "loops-and-repetition",
            ["attack-of-the-angry-snowballs", "robot-patrol-challenge", "the-floor-is-definitely-lava"],
            ["conditions-and-decisions", "variables-and-state", "feedback"],
        ),
        "conditions-and-decisions": topic_entry(
            "Conditions and Decisions",
            "A condition is a question with a true or false answer. The answer decides which code runs.",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "Has the player reached safety? Is the quiz answer correct? Is the wall closer than 15 centimetres? "
                "Each question turns information into a decision the program can repeat reliably."
            ),
            [
                ("Boolean question", "A test whose answer is true or false."),
                ("If", "Run these commands when the test is true."),
                ("If / else", "Choose one of two paths."),
                ("Comparison", "Check whether two values are equal or which one is larger."),
            ],
            (
                "A thermostat compares the room temperature with a target. Below the target it heats; "
                "above it, it waits. The chosen boundary controls the behaviour."
            ),
            [
                ("Quiz answer", "Compare the response with the stored answer."),
                ("Safe zone", "Set the game to WON when the player reaches the target."),
                ("Obstacle check", "Turn when the distance reading falls below a limit."),
                ("Fuel warning", "Show a warning when fuel drops below the chosen threshold."),
            ],
            [
                ("Checking once", "The program tests a changing condition only when the game starts."),
                ("Reversed comparison", "The warning appears above the threshold instead of below it."),
                ("Overlapping outcomes", "Win and loss can both become true without a priority rule."),
                ("Missing starting value", "The condition reads a variable that was never initialized."),
            ],
            (
                "Ask your child to say the condition as a question, then show what happens for true and false. "
                "That explanation usually reveals a reversed comparison faster than staring at the blocks."
            ),
            "conditions-and-decisions",
            ["quiz-of-questionable-knowledge", "escape-from-the-giant-pigeon", "robot-patrol-challenge"],
            ["sensing-and-collision", "variables-and-state", "autonomy"],
        ),
        "variables-and-state": topic_entry(
            "Variables and State",
            "A variable stores a value that can change. State records which set of rules currently applies.",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "Scores, timers, fuel, pet moods, and robot modes all have to be remembered. Giving each value "
                "a clear name lets a student inspect it while the project runs."
            ),
            [
                ("Name", "The variable name says what the value represents."),
                ("Initial value", "The project sets a known value before the test begins."),
                ("Update", "A particular event changes the value."),
                ("State", "A label such as PLAYING, CAUGHT, or DELIVERING selects the current rules."),
            ],
            (
                "A taxi meter keeps the current fare while the vehicle moves. A game score or robot mode "
                "also stores information now so that another rule can use it later."
            ),
            [
                ("Score", "Add one when an action finishes, rather than on every frame."),
                ("Pet mood", "Store a changing need and let it affect the pet's behaviour."),
                ("Game state", "Use STARTING, PLAYING, WON, and LOST to control separate rules."),
                ("Robot mode", "Record whether the machine is waiting, moving, or recovering."),
            ],
            [
                ("No reset", "A new game inherits the score or mode from the previous run."),
                ("Several scripts update one value", "The score jumps because more than one rule changes it."),
                ("Vague names", "Variables called thing or number make the code harder to read."),
                ("Hiding the display", "Removing a variable monitor from the stage does not erase its value."),
            ],
            (
                "A variable is understood when a student can trace three places: where it receives its starting "
                "value, what changes it, and which rules read it."
            ),
            "variables-and-score",
            ["the-suspiciously-emotional-space-pet", "grandmas-intergalactic-taxi", "microbit-reaction-timer"],
            ["conditions-and-decisions", "loops-and-repetition", "debugging"],
        ),
        "sensing-and-collision": topic_entry(
            "Sensing and Collision",
            "Sensing blocks report contact, colour, distance, button presses, and other changes a program can use.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "A moving sprite needs to notice walls, hazards, and targets. A robot needs a reading from outside "
                "its command list before it can respond to a box placed in its path."
            ),
            [
                ("Signal", "Information the program can read."),
                ("Collision", "Two defined areas touch or overlap."),
                ("Boundary", "A position or region where the rules change."),
                ("Continuous checking", "A loop reads changing input again and again."),
            ],
            (
                "A door sensor may use a physical switch; a game uses the shapes of two costumes. In both cases, "
                "the designer has to define exactly what counts as contact."
            ),
            [
                ("Touching colour", "Use a map colour to mark a wall or hazard."),
                ("Sprite collision", "Check whether the player and target overlap."),
                ("Distance reading", "Respond when an obstacle is nearer than a set limit."),
                ("Button sensing", "Read whether a physical control is pressed."),
            ],
            [
                ("Surprising collision area", "A costume is larger than it looks, so contact happens too early."),
                ("One-time check", "The player moves after the collision test has already finished."),
                ("Repeated scoring", "One long contact adds a point on every trip through the loop."),
                ("Trusting the picture", "The sprites look close, but the sensing block reports something else."),
            ],
            (
                "If one collision adds ten points, the sensor may be working perfectly. The response runs on every "
                "trip through the loop, so the student needs a state change or a reset before another point can score."
            ),
            "sensing-and-collision",
            ["the-floor-is-definitely-lava", "astro-chicken-rescue", "button-and-buzzer-alarm"],
            ["coordinates", "conditions-and-decisions", "sensors"],
        ),
        "input-and-output": topic_entry(
            "Input and Output",
            "Input enters a system. The code handles it, and an output makes the result visible, audible, or physical.",
            "Project connection",
            ["scratch", "robotics", "roblox"],
            (
                "A key press can move a sprite. A button can light an LED or sound a buzzer. Students identify "
                "the signal coming in, then write the rule that produces the response."
            ),
            [
                ("Input", "A signal or value the program can read."),
                ("Processing", "The rule applied to that information."),
                ("Output", "The resulting movement, light, sound, or display."),
                ("Mapping", "The chosen connection between an input and its response."),
            ],
            (
                "A doorbell turns a button press into sound. A keyboard game does the same sort of work "
                "with keys and sprites; a microcontroller uses pins, LEDs, motors, and buzzers."
            ),
            [
                ("Keyboard to movement", "Connect four keys to changes in x and y."),
                ("Button to buzzer", "Play a sound when a button is pressed."),
                ("Timer to display", "Show the measured time as a number."),
                ("Sensor to motor", "Change the motor command after a reading crosses a threshold."),
            ],
            [
                ("Input never read", "The output code exists, but nothing checks the control."),
                ("Competing inputs", "Two controls try to set the same output with no priority rule."),
                ("Wrong pin or object", "The code listens somewhere other than where the component is connected."),
                ("Silent response", "There is no visible sign that the input was received."),
            ],
            (
                "A finished project should make three parts easy to demonstrate: the input, the rule that handles it, "
                "and the output. The wiring may take a little longer to explain."
            ),
            "robot-commands-and-sequences",
            ["button-and-buzzer-alarm", "led-traffic-light", "robot-hamster-command-centre"],
            ["events-and-commands", "sensors", "feedback"],
        ),
        "debugging": topic_entry(
            "Debugging",
            "Debugging begins with a precise difference: what should have happened, and what happened instead?",
            "Project connection",
            ["scratch", "robotics", "roblox", "ai"],
            (
                "Guessing becomes expensive as a project grows. Students reproduce the problem, inspect a relevant "
                "value, choose one possible cause, and run a test that can prove them wrong."
            ),
            [
                ("Expected result", "Write down what should happen before editing."),
                ("Observed result", "Describe what happened, without adding a guessed cause."),
                ("Hypothesis", "Name one possible explanation."),
                ("Controlled test", "Inspect or change one thing that bears on that explanation."),
            ],
            (
                "If a bicycle chain slips only in one gear, that detail matters. A useful game bug report works "
                "the same way: it records the exact state and actions that produce the fault."
            ),
            [
                ("Show coordinates", "Read x and y when movement goes wrong."),
                ("Display state", "Check whether the game records PLAYING, WON, or LOST."),
                ("Test a smaller part", "Run one sprite, sensor, or rule by itself."),
                ("Reproduce the bug", "Find a sequence that makes the same problem happen again."),
            ],
            [
                ("Editing several scripts", "The bug disappears, but the useful evidence disappears with it."),
                ("Trying only the happy path", "The centre of the stage works while the edge remains broken."),
                ("Blaming Scratch", "A mistaken sign or state rule is left unexamined."),
                ("Covering the symptom", "Extra blocks hide the fault without correcting the underlying value."),
            ],
            (
                "A useful bug report gives the shortest steps that reproduce the fault and records a relevant value. "
                "Finding that evidence is good debugging, even before the repair is known."
            ),
            "debugging-clues",
            ["escape-from-the-giant-pigeon", "robot-maze-logic", "microbit-reaction-timer"],
            ["variables-and-state", "feedback", "conditions-and-decisions"],
        ),
        "sensors": topic_entry(
            "Sensors",
            "A sensor measures something in the physical world and gives the program a value to read.",
            "Project connection",
            ["robotics", "ai"],
            (
                "A robot can measure distance, light, motion, temperature, touch, or sound. The readings vary, "
                "so students collect several before choosing the threshold that controls a response."
            ),
            [
                ("Measurement", "A number or state reported by the sensor."),
                ("Threshold", "The chosen value where the program changes its response."),
                ("Noise", "Small fluctuations and errors in the readings."),
                ("Sampling", "Taking new readings as the signal changes over time."),
            ],
            (
                "An automatic light receives a number from its sensor. The designer decides which readings count "
                "as dark enough, and the code compares every new reading with that threshold."
            ),
            [
                ("Button", "Report one of two states: pressed or released."),
                ("Distance", "Estimate how far away an obstacle is."),
                ("Light level", "Return a changing value as a space becomes brighter or darker."),
                ("Accelerometer", "Report acceleration values that can indicate movement or orientation."),
            ],
            [
                ("Expecting a fixed reading", "Small fluctuations make the output flicker on and off."),
                ("Unhelpful threshold", "The chosen boundary does not fit the room or task."),
                ("Skipping calibration", "The program assumes every device and room gives the same values."),
                ("Giving the sensor too much credit", "The component supplies a reading; the student's code decides what to do with it."),
            ],
            (
                "A clear explanation names what the sensor measures, gives several readings from testing, and shows "
                "where the threshold is set. A lone number such as 347 needs rather more context."
            ),
            "sensors-as-questions",
            ["button-and-buzzer-alarm", "microbit-reaction-timer", "robot-patrol-challenge"],
            ["input-and-output", "feedback", "autonomy"],
        ),
        "feedback": topic_entry(
            "Feedback",
            "In a feedback loop, a system checks the result of an action before deciding what to do next.",
            "Project connection",
            ["robotics", "scratch", "ai"],
            (
                "A robot turns, reads the sensor again, and decides whether the correction helped. A game can "
                "check position after movement and return a player who has crossed the boundary."
            ),
            [
                ("Goal", "The position or result the system is trying to reach."),
                ("Observation", "A measurement of the current result."),
                ("Difference", "The gap between the measurement and the goal."),
                ("Correction", "An action chosen to reduce the gap."),
            ],
            (
                "A cyclist looks ahead and makes many small steering corrections. A robot patrol uses sensor "
                "readings instead of eyesight, but it also has to check what happened after each turn."
            ),
            [
                ("Boundary correction", "Return a sprite after its coordinates leave the allowed area."),
                ("Line following", "Adjust the steering after each surface reading."),
                ("Speed control", "Compare the measured speed with a target and change the motor command."),
                ("Visible game state", "Use sound or text to show whether a rule has fired."),
            ],
            [
                ("No second measurement", "The system keeps correcting without checking whether the first change helped."),
                ("Correction too large", "The result overshoots the goal and swings back the other way."),
                ("Slow feedback", "The new reading arrives too late to guide the next action."),
                ("Unclear goal", "There is no target value against which to judge the result."),
            ],
            (
                "Look for the whole loop: a goal, an action, a new measurement, and a correction based on that "
                "measurement. One blind correction is only a command."
            ),
            "robot-patrol-logic",
            ["robot-patrol-challenge", "microbit-reaction-timer", "the-floor-is-definitely-lava"],
            ["sensors", "loops-and-repetition", "autonomy"],
        ),
        "autonomy": topic_entry(
            "Autonomy",
            "An autonomous system selects actions from its inputs, rules, current state, and goal.",
            "Available later connection",
            ["robotics", "ai"],
            (
                "This later topic brings together sensing, conditions, loops, state, feedback, and testing. "
                "Students examine exactly which decisions the machine makes and which remain with its designer or user."
            ),
            [
                ("Goal", "The result the system is meant to reach or maintain."),
                ("Policy", "Rules that connect observations with actions."),
                ("State", "Information kept from one decision to the next."),
                ("Human boundary", "The choices and limits set by a person."),
            ],
            (
                "A robot vacuum chooses movements from sensor readings, but people still set its goal, rules, "
                "working area, and stop controls. Its autonomy is real and quite narrow."
            ),
            [
                ("Patrol rule", "Choose a turn after an obstacle reading."),
                ("Game opponent", "Select an action from the player's distance and current game state."),
                ("Recovery behaviour", "Return to a safe mode after an error."),
                ("Stop condition", "End the action when a boundary or goal is reached."),
            ],
            [
                ("Mistaking a sequence for autonomy", "A fixed route never changes when new information arrives."),
                ("No stop rule", "The system continues after its goal or safe boundary has been reached."),
                ("Claiming understanding", "A successful rule is described as if the machine knows why it works."),
                ("One perfect test", "The system fails as soon as an obstacle moves or a reading changes."),
            ],
            (
                "This topic comes later, after separate work with commands, sensors, decisions, state, and feedback. "
                "The important distinction is which choices the machine makes and which limits a person has set."
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
            "A coordinate change has a visible result. Students can predict where a sprite will land, define the edge "
            "of a map, and read the x and y displays when the movement goes wrong."
        ),
        "logic_kernel": TOPICS["coordinates"]["math_kernel"],
        "real_world_story": (
            "Maps, screen layouts, robot navigation, drones, and computer vision all represent position with numbers. "
            "The dimensions and coordinate systems change, but the need for a shared reference point remains."
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
        "age_language": "No previous experience is required. The final challenge can stretch students who have done this before.",
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
    ("0-10 min", "Set up the problem", "Agree on what the finished system needs to do."),
    ("10-30 min", "Try the idea", "Use short examples to see the rule on its own."),
    ("30-65 min", "Build together", "Put the rule to work in the guided project."),
    ("65-80 min", "Change one thing", "Predict what a modification will do, then test it."),
    ("80-90 min", "Demonstrate and save", "Show the result, explain one decision, and save the project."),
]


LESSONS.update(
    {
        "events-and-commands": lesson_entry(
            "What Makes a Program Start?",
            "scratch",
            "events-and-commands",
            "The robot hamster has five perfectly good commands and no idea when to begin. Give it a trigger, arrange the commands, and see how one change in order alters the route.",
            ["Match an event with its response.", "Put commands in a deliberate order.", "Predict a short sequence before running it.", "Keep setup separate from repeated actions.", "Explain one cause-and-effect link in the program."],
            [("when green flag clicked", "set the starting state"), ("when space key pressed", "respond to one chosen input"), ("broadcast START", "tell another script to begin"), ("move / turn / wait", "make an ordered route")],
            "robot-hamster-command-centre",
            ["The student can point to the trigger.", "A three-command sequence is predicted before it runs.", "Restarting produces the same setup.", "Each event has a clear job.", "The student changes the order and explains the result."],
            ["The commands are present, but no event starts them.", "The hamster moves before its position is reset.", "Two scripts try to control the same action.", "Timing is changed before the command order is checked."],
            [{"name": "Builder", "ideas": ["Add a second command key."]}, {"name": "Inventor", "ideas": ["Broadcast a mission-complete event."]}, {"name": "Boss Level", "ideas": ["Build a queue of commands before execution."]}],
            ["What event starts the program?", "Which command runs first?", "What changed when the order changed?", "Which part is setup?", "What did you debug?"],
            "The class connected events to short command sequences. Students predicted an order, ran it, and then moved one command to see exactly how the hamster's route changed.",
        ),
        "loops-and-repetition": lesson_entry(
            "How Many Times Should the Snowballs Attack?",
            "scratch",
            "loops-and-repetition",
            "One snowball is an inconvenience. Fifty copied snowball scripts are a maintenance problem. Put the attack in a loop, control its timing, and give it a reason to stop.",
            ["Spot instructions that repeat.", "Choose between repeat, forever, and repeat-until.", "Count iterations.", "Control the pace of a loop.", "Point to the rule that stops it."],
            [("repeat 10", "run ten waves"), ("forever", "keep checking for the life of the game"), ("repeat until score = 8", "stop when the goal is reached"), ("wait 0.5 seconds", "leave time between iterations")],
            "attack-of-the-angry-snowballs",
            ["Copied blocks have been replaced by a loop.", "The student predicts how many times it will run.", "Something inside the loop changes each time.", "The game has a clear stop or state rule.", "The student adjusts the timing independently."],
            ["Blocks beneath a forever loop never run.", "Nothing inside repeat-until can make its condition true.", "Hazards appear too quickly to play or inspect.", "Starting values are reset during every wave."],
            [{"name": "Builder", "ideas": ["Add a fixed second wave."]}, {"name": "Inventor", "ideas": ["Shorten the delay as score rises."]}, {"name": "Boss Level", "ideas": ["Create wave states with different patterns."]}],
            ["What repeats?", "How many times?", "What changes each time?", "What stops the loop?", "Which repeated copy did you remove?"],
            "The snowball game now uses loops instead of copied code. The class compared fixed repetition with continuous checking, then adjusted the delay and stopping condition to keep it playable.",
        ),
        "conditions-and-decisions": lesson_entry(
            "How Does a Game Decide?",
            "scratch",
            "conditions-and-decisions",
            "The Quiz of Questionable Knowledge has received the answer 'moon cheese.' Its code must decide whether that is correct, give useful feedback, and move on without awarding seventeen points.",
            ["Write a rule as a true-or-false question.", "Use if and if/else.", "Compare text and numbers.", "Resolve decisions that can overlap.", "Explain why a particular branch ran."],
            [("if answer = 'Ottawa'", "compare text for equality"), ("if score > 5", "compare a number with a threshold"), ("if touching danger", "use a sensing result"), ("else", "handle the other answer")],
            "quiz-of-questionable-knowledge",
            ["The student states the condition as a question.", "Both the true and false paths can be shown.", "The comparison uses the intended value and type.", "Each question can score only once.", "The student adds one decision independently."],
            ["Using assignment language instead of comparison.", "Checking a changing condition only once.", "Two branches score the same answer.", "An else belongs to the wrong if."],
            [{"name": "Builder", "ideas": ["Add feedback for a wrong answer."]}, {"name": "Inventor", "ideas": ["Accept two equivalent spellings."]}, {"name": "Boss Level", "ideas": ["Choose question difficulty from score."]}],
            ["What question does the code ask?", "What makes it true?", "What happens otherwise?", "Can two outcomes happen together?", "What rule did you add?"],
            "The quiz gave students several kinds of decisions to write and test. They compared answers, handled the alternative path, and traced the condition responsible when the wrong branch ran.",
        ),
        "variables-and-score": lesson_entry(
            "Where Does the Score Live?",
            "scratch",
            "variables-and-state",
            "The space pet insists it was fed, but the program has forgotten. Give its needs names, decide what changes them, and make every new game start with a clean memory.",
            ["Give a variable a useful name.", "Set its starting value.", "Update it when a particular event occurs.", "Read it in a condition.", "Distinguish the stored value from its on-screen display."],
            [("set mood to 5", "give mood a starting value"), ("change mood by -1", "update mood over time"), ("if mood < 2", "make a decision from the stored value"), ("set game_state to PLAYING", "record the current mode")],
            "the-suspiciously-emotional-space-pet",
            ["The variable name describes what it stores.", "Restarting restores the initial value.", "One event changes the value once.", "At least one condition reads the value.", "The student can explain the current state."],
            ["Variable never resets.", "Several scripts change the score unexpectedly.", "A display is hidden but the value remains.", "Text and number values are compared accidentally."],
            [{"name": "Builder", "ideas": ["Add a second need such as energy."]}, {"name": "Inventor", "ideas": ["Make needs affect each other."]}, {"name": "Boss Level", "ideas": ["Create named pet states from several variables."]}],
            ["What does the variable remember?", "Where is it initialized?", "Which event changes it?", "Which decision reads it?", "What state is active now?"],
            "The space pet's changing needs are stored in named variables. Each value has a starting point, a reason to change, and at least one rule that reads it; restarting clears the old state.",
        ),
        "sensing-and-collision": lesson_entry(
            "How Does the Game Know You Touched the Lava?",
            "scratch",
            "sensing-and-collision",
            "The floor is convincingly lava-coloured. The computer remains unmoved. Define what counts as danger, check it while the player moves, and make one collision cause one result.",
            ["Identify the signal used for sensing.", "Define a collision or boundary.", "Check a changing signal inside a loop.", "Prevent one contact from scoring repeatedly.", "Inspect the sensing result while debugging."],
            [("touching Lava?", "check contact with a sprite"), ("touching colour red?", "check a coloured region of the map"), ("distance to hazard < 40", "compare distance with a limit"), ("if touching then set state", "change the game after contact")],
            "the-floor-is-definitely-lava",
            ["The student can show the collision area.", "Sensing continues while the player moves.", "One contact causes one state change.", "Restarting clears the collision state.", "A fast crossing of the boundary has been tested."],
            ["Costume transparency makes the hitbox surprising.", "Contact is checked only at startup.", "Score rises every frame during one collision.", "A visual overlap is assumed without reading the sensing result."],
            [{"name": "Builder", "ideas": ["Add one safe platform."]}, {"name": "Inventor", "ideas": ["Make platforms move while preserving collision."]}, {"name": "Boss Level", "ideas": ["Create one-way or temporary safe surfaces."]}],
            ["What signal counts as contact?", "How often is it checked?", "What state changes?", "How did you test the boundary?", "What collision bug did you fix?"],
            "The lava game checks a defined contact signal while the player moves, then changes state after a collision. Students also tested the awkward cases: costume edges and fast boundary crossings.",
        ),
        "debugging-clues": lesson_entry(
            "What Is the Bug Trying to Tell You?",
            "scratch",
            "debugging",
            "The game fails only when the player reaches safety while being caught near the right edge. Random edits have made it stranger. Reproduce the fault, inspect the game state, and test one possible cause.",
            ["Describe the expected and observed results separately.", "Reproduce a bug with a short sequence of actions.", "Inspect a relevant value or state.", "Choose one possible cause.", "Run a controlled test and explain the evidence."],
            [("show x position", "read the movement value"), ("say game_state", "make the hidden mode visible"), ("disable one script", "test a smaller system"), ("repeat the same inputs", "check that the fault is reproducible")],
            "escape-from-the-giant-pigeon",
            ["The student describes the fault without guessing at its cause.", "A repeatable sequence triggers it.", "At least one relevant value is inspected.", "Only one hypothesis is tested at a time.", "The repair is explained from the evidence."],
            ["Several scripts are changed before the next test.", "Only the easiest successful path is tried.", "A delay hides a state problem for a moment.", "Testing stops after the symptom disappears once."],
            [{"name": "Builder", "ideas": ["Create a bug report with exact steps."]}, {"name": "Inventor", "ideas": ["Add temporary on-screen state monitors."]}, {"name": "Boss Level", "ideas": ["Design an automated edge-case test sequence."]}],
            ["What should happen?", "What actually happens?", "How can you reproduce it?", "What evidence did you inspect?", "Why did the fix work?"],
            "The class worked from a repeatable bug rather than a clean project. Students recorded what happened, displayed the relevant position and state, and changed one thing at a time until the evidence supported a repair.",
        ),
        "robot-commands-and-sequences": lesson_entry(
            "Can a Robot Follow Your Instructions?",
            "robotics",
            "input-and-output",
            "A delivery robot has been told to 'go around the chair.' That instruction works on people and fails on robots. Replace it with measured moves and turns that can be checked on a grid.",
            ["Break a route into commands the robot can execute.", "Order moves and turns.", "Predict the final position and direction.", "Test the route on paper or in simulation.", "Revise one faulty command."],
            [("forward 2", "move two grid units"), ("turn right", "change direction without changing position"), ("pause", "separate actions so they can be observed"), ("repeat route", "reuse a tested sequence")],
            "robot-maze-logic",
            ["Each command has one clear meaning.", "The student predicts before running the route.", "Direction is recorded after every turn.", "The route reaches the target.", "One revision is justified from the failed test."],
            ["The route contains phrases the robot cannot execute.", "Direction is lost after a turn.", "Several route steps are changed after one failure.", "The plan treats the robot as a point with no width."],
            [{"name": "Builder", "ideas": ["Add one obstacle and reroute."]}, {"name": "Inventor", "ideas": ["Create reusable route segments."]}, {"name": "Boss Level", "ideas": ["Write a route checker for a grid map."]}],
            ["What is the goal?", "Which command runs first?", "Where does the robot face now?", "Which command failed?", "How did the revision change the route?"],
            "The route turns 'go around the chair' into measured moves and turns. Students tracked position and direction on a grid, predicted the destination, and revised the first command that failed. This lesson can be done on paper or in simulation.",
        ),
        "sensors-as-questions": lesson_entry(
            "What Question Is the Sensor Answering?",
            "robotics",
            "sensors",
            "The display says 347. That might mean bright, close, tilted, or nothing useful at all. Find out what the sensor measures, collect readings, and decide where the program should change its response.",
            ["Name the quantity a sensor measures.", "Record a changing value.", "Choose and test a threshold.", "Separate the measurement from the program's decision.", "Explain variation in the readings."],
            [("button = pressed", "read one of two states"), ("distance < 15", "compare a reading with a threshold"), ("light level", "inspect a value that changes"), ("read repeatedly", "take several samples over time")],
            "microbit-reaction-timer",
            ["The student names the measured quantity.", "Several readings have been recorded.", "A threshold is stated and tested.", "The output changes for a traceable reason.", "The student identifies one limitation of the reading."],
            ["Every reading is expected to be identical.", "A threshold is chosen from one test.", "The sensor is credited with making the decision.", "The output changes before the input values are recorded."],
            [{"name": "Builder", "ideas": ["Display raw readings before deciding."]}, {"name": "Inventor", "ideas": ["Compare two candidate thresholds."]}, {"name": "Boss Level", "ideas": ["Smooth several readings before acting."]}],
            ["What does the sensor measure?", "What values did you observe?", "Where is the threshold?", "What does the code decide?", "When could the reading be wrong?"],
            "Several sensor readings were recorded before the class chose a threshold. Students kept the measurement separate from the code's decision and noted why repeated tests may produce slightly different numbers.",
        ),
        "robot-patrol-logic": lesson_entry(
            "How Can a Robot Patrol Without Getting Stuck?",
            "robotics",
            "feedback",
            "The patrol route works until somebody moves a box into it. Add a distance check, choose a recovery action, and make the robot test the route again instead of turning forever.",
            ["Combine a repeated patrol with sensor readings.", "Use a condition to choose a correction.", "Record the patrol's current state.", "Test an obstacle at an awkward point in the route.", "Trace the sense-decide-act loop."],
            [("repeat patrol", "continue along the route"), ("if obstacle near", "decide when the plan must change"), ("turn and check again", "measure after the correction"), ("state = RECOVERING", "record the current mode")],
            "robot-patrol-challenge",
            ["The normal patrol route works.", "An obstacle causes a different action.", "The robot reads the sensor again after correcting.", "Recovery cannot become an endless turn.", "The student traces the sense-decide-act cycle."],
            ["The patrol loop never reads the sensor.", "One obstacle leaves the robot permanently in recovery mode.", "The robot keeps turning without a new reading.", "There is no rule for ending the patrol."],
            [{"name": "Builder", "ideas": ["Stop and signal at an obstacle."]}, {"name": "Inventor", "ideas": ["Try a second route after turning."]}, {"name": "Boss Level", "ideas": ["Track failed directions and choose a recovery state."]}],
            ["What repeats during patrol?", "What does the system sense?", "Which condition changes the plan?", "How does it check the correction?", "What limit remains?"],
            "The patrol can respond when a box appears on its route. It reads a sensor, chooses a correction, records that it is recovering, and checks again before returning to patrol mode.",
        ),
    }
)


LESSON_TIMELINES = {
    "events-and-commands": [
        ("0-10 min", "A route with no start", "Run the command list without an event and identify what is missing."),
        ("10-25 min", "Triggers and order", "Connect short command sequences to the flag, a key, and a message."),
        ("25-65 min", "Build the hamster route", "Set a known start, add controls, and run an ordered patrol."),
        ("65-80 min", "Move one command", "Change the order, predict the new route, and check the result."),
        ("80-90 min", "Show the cause", "Demonstrate which event starts the route and which command changed it."),
    ],
    "loops-and-repetition": [
        ("0-10 min", "Find the repeated work", "Mark the snowball actions that would otherwise be copied."),
        ("10-25 min", "Compare three loops", "Try repeat, forever, and repeat-until with short visible examples."),
        ("25-65 min", "Build the attack", "Create the fall-and-reset cycle, then add catches, misses, and waves."),
        ("65-80 min", "Tune the repetition", "Change the delay or stopping condition and test whether the game remains playable."),
        ("80-90 min", "Explain the loop", "Show what repeats, what changes each time, and what makes it stop."),
    ],
    "conditions-and-decisions": [
        ("0-10 min", "Write the question", "Turn one quiz rule into a question with a true or false answer."),
        ("10-25 min", "Test both branches", "Compare text and numbers, then run the true and false cases."),
        ("25-65 min", "Build the quiz", "Add questions, feedback, score, and question state."),
        ("65-80 min", "Try awkward answers", "Test capitals, wrong answers, and inputs that should not score twice."),
        ("80-90 min", "Trace one decision", "Demonstrate the condition and explain why its branch ran."),
    ],
    "variables-and-score": [
        ("0-10 min", "What must the pet remember?", "Choose two changing needs and give each one a useful name."),
        ("10-25 min", "Start, change, read", "Set a value, update it from an event, and use it in a condition."),
        ("25-65 min", "Build the pet", "Add care actions, time-based change, and a visible state."),
        ("65-80 min", "Break the reset", "Create a stale value deliberately, then repair the initialization."),
        ("80-90 min", "Follow one value", "Show where a variable starts, what changes it, and which rule reads it."),
    ],
    "sensing-and-collision": [
        ("0-10 min", "Define contact", "Decide exactly which sprite or colour counts as safe and dangerous."),
        ("10-25 min", "Read the sensor", "Compare visible overlap with the value reported by a sensing block."),
        ("25-65 min", "Build the lava room", "Add movement, jumping, platforms, collision, and game state."),
        ("65-80 min", "Test the edges", "Try costume boundaries, fast crossings, and contact that lasts several frames."),
        ("80-90 min", "Show one collision", "Demonstrate the signal, the state change, and a repaired boundary case."),
    ],
    "debugging-clues": [
        ("0-15 min", "Reproduce the fault", "Record the shortest sequence that produces the wrong ending."),
        ("15-30 min", "Expose the state", "Display a relevant coordinate or game-state value."),
        ("30-55 min", "Test one explanation", "Choose one possible cause and make a controlled test."),
        ("55-75 min", "Repair and retest", "Make the smallest useful change, then repeat the original sequence."),
        ("75-90 min", "Give the bug report", "Show the fault, the evidence, the repair, and a regression test."),
    ],
    "robot-commands-and-sequences": [
        ("0-10 min", "Replace vague directions", "Turn 'go around the chair' into commands the robot can execute."),
        ("10-25 min", "Predict on the grid", "Track position and direction through a short route."),
        ("25-60 min", "Build the maze route", "Define a command set, start state, target, and complete sequence."),
        ("60-80 min", "Repair the first mismatch", "Trace the route and change the earliest command that fails."),
        ("80-90 min", "Hand over the instructions", "Have another student follow the route and explain the revision."),
    ],
    "sensors-as-questions": [
        ("0-10 min", "Name the measurement", "Identify what the input reports and the units or states it uses."),
        ("10-30 min", "Collect readings", "Record several values under different known conditions."),
        ("30-45 min", "Choose a boundary", "Compare readings and test a threshold or timing rule."),
        ("45-75 min", "Build the reaction timer", "Add waiting, a random start, button input, and an elapsed-time result."),
        ("75-90 min", "Explain the limits", "Demonstrate the reading, the program's decision, and one source of variation."),
    ],
    "robot-patrol-logic": [
        ("0-15 min", "Make the normal route work", "Define a short patrol with a known start and stop rule."),
        ("15-30 min", "Add the obstacle question", "Choose the signal and condition that interrupt the patrol."),
        ("30-60 min", "Build recovery", "Record the new state, act, and read the sensor again."),
        ("60-80 min", "Set traps", "Test a corner, repeated obstacle, and recovery that might loop forever."),
        ("80-90 min", "Trace the feedback", "Show the sense-decide-act cycle and state one limit."),
    ],
}


TOPIC_QUESTIONS = {
    "events-and-commands": "What starts the program, and which command runs next?",
    "coordinates": "Where am I, and how does a number move me?",
    "loops-and-repetition": "What repeats, and what makes it stop?",
    "conditions-and-decisions": "Which true-or-false question chooses the next branch?",
    "variables-and-state": "What must the project remember, and when does it change?",
    "sensing-and-collision": "What exactly counts as contact?",
    "input-and-output": "What enters the system, and what response comes out?",
    "debugging": "What evidence explains the difference?",
    "sensors": "What exactly is the machine measuring?",
    "feedback": "Did the action move the result towards the goal?",
    "autonomy": "Which choices does the machine make, and which limits did a person set?",
}


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
    if lesson_slug in LESSON_TIMELINES:
        lesson["timeline"] = LESSON_TIMELINES[lesson_slug]
    lesson.setdefault("timeline", STANDARD_TIMELINE)
    lesson["slug"] = lesson_slug
    lesson["url"] = f"/lessons/{lesson_slug}"
    punctuation = "" if lesson["title"].endswith((".", "?", "!")) else "."
    lesson.setdefault(
        "meta_description",
        f"{lesson['title']}{punctuation} A 90-minute School of Code lesson for {lesson['program']}, with examples, a guided build, checkpoints, and challenges.",
    )

for topic_slug, topic in TOPICS.items():
    topic["central_question"] = TOPIC_QUESTIONS[topic_slug]
    topic["slug"] = topic_slug
    topic["url"] = f"/topics/{topic_slug}"
    topic.setdefault("meta_description", f"A School of Code guide to {topic['title'].lower()}, with examples, common bugs, and related projects and lessons.")


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
