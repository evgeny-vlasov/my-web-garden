def article(title, category, description, introduction, sections, related):
    return {
        "title": title,
        "category": category,
        "description": description,
        "introduction": introduction,
        "sections": sections,
        "related": related,
        "author": "School of Code",
    }


BLOG_POSTS = {
    "is-coding-class-just-more-screen-time": article(
        "Is Coding Class Just More Screen Time?",
        "Parent Guides",
        "The useful question is what a child does at the screen: watch, or make something that can be tested and changed.",
        (
            "An hour with a computer can mean an endless feed. It can also mean building a game, predicting where a sprite will land, "
            "finding a collision bug, and showing someone else how the score works. The clock sees two hours of screen time. The child is doing very different work."
        ),
        [
            (
                "Watch the work",
                [
                    "In a coding class, students make decisions that alter a system. If the player starts in the wrong corner, they inspect the x and y values. If winning and losing happen at once, they find the rules that are competing. The program follows the instructions it has, including the mistaken ones, and gives the student something definite to investigate.",
                    "That resistance matters. A video continues whether the viewer understands it or not. A game with broken movement does not. To fix it, the student has to compare intention with evidence and revise the rule."
                ],
            ),
            (
                "Ask for a tour",
                [
                    "After class, ask the student to open the project and show how it works. A small game, robot route, reaction timer, or state diagram is enough. Then ask a concrete question: What starts the program? Which number controls left and right? What went wrong today? What did you change?",
                    "A finished project does not prove that every line was written alone or that every idea is mastered. It does give the conversation an object. The student can point to a rule, run a test, and explain a choice instead of reporting that class was simply ‘good.’"
                ],
            ),
            (
                "Try one small change",
                [
                    "Change the player speed, move a safe zone, or make the score begin at five. If the student can predict the result and find the relevant part of the program, the project has become something they can work on rather than something they merely operated.",
                    "Ask about a failure too. Real projects accumulate wrong turns: x changes instead of y, a loop runs forever, or restart keeps an old value. Describing the repair is often more revealing than showing the polished final run."
                ],
            ),
            (
                "Boundaries still matter",
                [
                    "Useful work at a computer does not make unlimited device use a good idea. A class needs a beginning, a task, checkpoints, and an ending. Students should talk to people, sketch on paper when it helps, take visual breaks, and save their work properly.",
                    "School of Code classes follow a planned sequence. Computer Lab time is for guided work on projects that already have a purpose. Neither is a licence for random gaming or browsing."
                ],
            ),
            (
                "A better measure",
                [
                    "Minutes are still worth counting, but they do not describe the whole activity. Ask whether the child made choices, encountered a real difficulty, inspected evidence, and left with a version that can be demonstrated. Those are visible differences between making and consuming.",
                    "A computer can be a television, but it can also be a workshop bench, notebook, stage, and test instrument. The useful question is which one it was today."
                ],
            ),
        ],
        [("For Parents", "/parents"), ("Computer Lab", "/computer-lab"), ("Escape from the Giant Pigeon", "/projects/escape-from-the-giant-pigeon")],
    ),
    "what-age-should-kids-start-programming": article(
        "What Age Should Kids Start Programming?",
        "Coding for Kids",
        "A suitable starting point depends on the child, the task, and the support available—not one universal birthday.",
        (
            "There is no birthday on which programming suddenly becomes appropriate. One young child may happily arrange commands with help; an older beginner may want to understand the whole point before touching the editor. A more useful question is: what kind of programming work fits this child now?"
        ),
        [
            (
                "Signs of readiness",
                [
                    "Beginners do not need fast typing, algebra, or a supply of technical words. Look for ordinary habits: following a short sequence, wanting to make something happen, noticing when the result differs from the plan, and being willing to try a second version.",
                    "These habits are not admission requirements carved in stone. A well-sized project helps develop them. The first working version should arrive before the child has spent the entire session wrestling with setup."
                ],
            ),
            (
                "Choose the right material",
                [
                    "Scratch removes much of the spelling and punctuation burden while keeping events, loops, conditions, variables, messages, and state. Students can think about why a character moves the wrong way without first hunting for a missing bracket. Logical errors remain, which is fortunate: they are where much of the programming lives.",
                    "Robotics can begin with a paper grid, a simulated route, buttons, or LEDs. Hardware is useful when it helps answer the question. It need not arrive on the first day carrying seventeen loose wires."
                ],
            ),
            (
                "Start with something finishable",
                [
                    "Four-direction movement, a two-state traffic light, or a short robot route can be a complete first task. The child meets one meaningful problem without also managing accounts, original artwork, hardware faults, and plans for a twelve-level epic.",
                    "Completion gives everyone something stable to discuss. Can the student explain one command? Follow a checkpoint? Ask a specific question? Try again after a mismatch? Those observations tell us more than a broad age chart."
                ],
            ),
            (
                "The same project can have more depth",
                [
                    "One student may make reliable movement. Another can add boundary handling, a second stage, or a pursuer that changes speed with distance. Both are working with coordinates, but the difficulty is different.",
                    "Group fit also depends on reading comfort, independence, previous experience, and whether the student will explain a problem aloud. Age is useful information; it is simply not the only information."
                ],
            ),
            (
                "How to choose a starting point",
                [
                    "Ask what the child wants to make. Stories can become interactive scenes. A fascination with systems can lead to traffic lights or robot mazes. A child who loves games may become interested when given control of the rules.",
                    "School of Code has not published a universal starting age while exact groups and schedules are still being prepared. A conversation about fit can use the child's interests and working habits to find a task that is neither automatic nor overwhelming.",
                    "A trial task should leave room for surprise. Some children who are impatient with step-by-step instructions will spend half an hour repairing a game they chose to make. Others love the idea but need shorter checkpoints or more time away from the screen. The first project is useful evidence, not a permanent label."
                ],
            ),
        ],
        [("Scratch program", "/programs/scratch"), ("Robotics program", "/programs/robotics"), ("Contact", "/contact")],
    ),
    "why-scratch-is-a-great-first-programming-language": article(
        "Why Scratch Is a Good First Programming Language",
        "Coding for Kids",
        "Scratch makes program structure visible and lets beginners work on logic before punctuation takes over the afternoon.",
        (
            "Scratch is often praised because its blocks fit together. That helps, but the more important feature is visibility. A beginner can see which event starts a script, what repeats, where a condition branches, and when a variable changes."
        ),
        [
            (
                "It postpones one kind of difficulty",
                [
                    "Typed syntax matters eventually. It is rarely the first idea a beginner needs. A missing quote or bracket can stop a program before the student has thought seriously about movement, collision, or state. Scratch removes many syntax errors while leaving the interesting logical ones intact.",
                    "A sprite can still walk backwards, score twice, or remain stuck after the game ends. Those failures concern the system the student meant to build, so the class can discuss the idea rather than spend the whole session policing punctuation."
                ],
            ),
            (
                "A small project can be complete",
                [
                    "Code, drawing, sound, keyboard input, and animation live in the same editor. That makes it possible to finish a modest game and still face real design decisions. Escape from the Giant Pigeon needs a known start, controls, a pursuer, safe areas, collision rules, win and loss states, and a reliable restart.",
                    "Coordinates now determine whether the player escapes. Conditions settle whether contact means safety or disaster. The project gives each concept a job."
                ],
            ),
            (
                "Simple blocks can hold deep systems",
                [
                    "A beginner can move a sprite with four keys. Later versions might add acceleration, screen wrapping, several maps, or controls that depend on game state. The blocks remain familiar while the relationships become more demanding.",
                    "Students can also replace the artwork and alter the rules. If pigeon, taxi, and chicken can change while events, movement, state, and tests remain recognizable, they are learning to separate a program's structure from its surface."
                ],
            ),
            (
                "What good Scratch teaching requires",
                [
                    "Dragging blocks is not automatically a programming lesson. Copying a finished stack without predicting, testing, or changing it teaches very little. A short script that a student can explain is more useful than a magnificent tower of mystery blocks.",
                    "The sprite library is not the curriculum either. Art and sound can support authorship, but the project needs a system that starts, changes, checks, remembers, or communicates. Students should be able to identify that system and make a deliberate modification."
                ],
            ),
            (
                "The blocks connect forward",
                [
                    "Events return as event handlers in other environments. Variables remain variables. Conditions, functions, messages, and state appear in Lua, Python, robotics, web programming, and game engines.",
                    "When students understand what the blocks express—why a loop stops or how state resets—text syntax becomes a new notation for familiar ideas. Scratch is a strong beginning because it makes those ideas available early, before typing accuracy has had a chance to ruin the afternoon.",
                    "This transition does not require students to abandon Scratch on a schedule. It remains useful for testing an animation, explaining an algorithm, or building a game quickly. Languages are tools, and a student who can choose a clear tool for the work is further ahead than one who has merely collected difficult-looking syntax."
                ],
            ),
        ],
        [("Scratch & Game Design", "/programs/scratch"), ("Topic library", "/topics"), ("Project library", "/projects#scratch-projects")],
    ),
    "why-debugging-is-good-for-kids": article(
        "Why Debugging Is Good for Kids",
        "Project-Based Learning",
        "Debugging turns ‘it doesn't work’ into a sequence of questions that can actually be answered.",
        (
            "A bug begins with a disagreement: the student expects one thing, and the program does another. Random clicking can blur that disagreement. Debugging makes it useful by asking what happened, what should have happened, and what evidence could separate the possible causes."
        ),
        [
            (
                "First, remove the verdict",
                [
                    "Children sometimes read a broken project as a judgment: I am bad at this, or the computer hates me. The computer is less dramatic. It has followed a rule, read a value, or entered a state. The task is to find which one.",
                    "A routine helps: describe the expected result, reproduce the actual one, and make the relevant state visible. Difficulty remains, but it has edges now."
                ],
            ),
            (
                "Change one useful thing",
                [
                    "Suppose a player can win and lose at the same moment. Adding waits to three scripts may hide the symptom. A cleaner test displays the game state, reproduces simultaneous contact, and shows which condition runs first.",
                    "One controlled change preserves information. If the result changes, there is evidence. If it does not, the failed guess has still ruled out a cause."
                ],
            ),
            (
                "Keep a tiny record",
                [
                    "Four lines are often enough: expected result, observed result, test, conclusion. A robot should face east after two turns; it faces north; tracing the commands reveals a left where a right belonged. No ceremonial paperwork is required.",
                    "The conclusion may be that the first theory was wrong. That is useful. Over time, students also recognize familiar patterns: unknown start, wrong sign, repeated event, stale state, loose connection, or noisy reading. Names make the search faster without replacing the current evidence."
                ],
            ),
            (
                "The habit travels",
                [
                    "A circuit stays dark: verify power and output, then inspect one connection. A robot turns too far: measure, compare, change one value, test again. A written argument has a gap: find the claim that the evidence does not support.",
                    "Programming offers unusually quick feedback. It runs the instructions the student actually gave, including assumptions that were never noticed."
                ],
            ),
            (
                "How adults can help",
                [
                    "Ask what was supposed to happen, what did happen, and which test would provide useful evidence. Point to a relevant value or suggest disabling one script if needed. Then leave the consequential change to the student.",
                    "The best demonstration is not always a spotless project. A student who can reproduce one bug and explain the repair has shown careful, independent thought in a practical form.",
                ],
            ),
            (
                "Keep the repair small",
                [
                    "Adults can model the same tone. Instead of asking who broke the project, ask when the behaviour changed and whether the old version still works. Save before a risky experiment. Give a strange result a name. Calm attention is more useful than rescue, and considerably more useful than announcing that the machine is stupid.",
                    "Debugging also teaches restraint. Once a student has evidence for one fault, the repair can stay small. Rebuilding the entire script may remove the symptom, but it makes the cause harder to understand and can create three fresh bugs for the price of one."
                ],
            ),
        ],
        [("Debugging topic", "/topics/debugging"), ("Debugging lesson", "/lessons/debugging-clues"), ("Our Method", "/method")],
    ),
    "robotics-for-kids-where-to-start": article(
        "Robotics for Kids: Where to Start",
        "Robotics for Kids",
        "Begin with a clear question about input, decisions, and output. The impressive robot can wait.",
        (
            "Robotics can conjure an expensive picture: autonomous machines, complex kits, and a table covered in parts no one quite remembers buying. The useful starting point is smaller. What can the system sense, what rule will it follow, and what will it do?"
        ),
        [
            (
                "Sense, decide, act",
                [
                    "A button-and-buzzer alarm fits this model. So does a simulated robot avoiding a wall. The input might be a button state or a distance reading; the program compares it with a rule; the buzzer or motor produces the output.",
                    "Keeping the parts separate prevents muddled explanations. A sensor measures. A motor acts. The program connects the measurement to a decision."
                ],
            ),
            (
                "Choose one question",
                [
                    "Can the robot follow an exact route? Can a button control a buzzer? Can an LED sequence move through safe states? Can a timer distinguish waiting from reacting? Each project exposes a different relationship.",
                    "Choosing the kit before the question often buries the lesson under assembly. A small system that students can explain is a better first project than a sophisticated machine whose behaviour stays opaque."
                ],
            ),
            (
                "Paper and simulation have jobs",
                [
                    "Robot Maze Logic can begin on a grid. Students record a starting direction, define forward and turn commands, predict a route, and trace it one command at a time. That is real work on decomposition, state, and debugging.",
                    "A traffic-light sequence can run on screen before it controls LEDs. A sensor rule can begin with sample values. Logic comes first; later, the loose wire or drifting motor becomes a particular problem instead of one large cloud of failure."
                ],
            ),
            (
                "Bring in the physical world deliberately",
                [
                    "Hardware earns its place when its behaviour matters. Connections fail, motors slip, sensors vary, and the floor refuses to match the perfect diagram. Students must decide whether to inspect code, wiring, measurement, or assumptions about the room.",
                    "Project descriptions should also be accurate about materials. Some activities work in simulation, some have optional physical versions, and a physical micro:bit timer requires a micro:bit. Equipment arrangements depend on the group."
                ],
            ),
            (
                "Autonomy comes later",
                [
                    "A machine following a fixed route is executing commands. A responsive patrol repeatedly checks changing information and chooses among defined actions. That adds sensing, conditions, state, and feedback.",
                    "Build the layers in view. A strong first demonstration ends with the student naming the input, the decision rule, the output, and one limit. The materials can become more elaborate after that model is clear.",
                ],
            ),
            (
                "Add one layer at a time",
                [
                    "Sequence matters more than spectacle. A route project can lead to repeat loops, then to a sensor stop, then to a recovery turn. Each addition answers a question raised by the earlier version. Students can see why the new idea is needed instead of meeting a finished robot whose inner life is concealed inside a large starter program.",
                    "Safety belongs in that sequence as well. Motors, power, tools, and loose components need rules suited to the actual equipment. Paper and simulation are sensible places for logic that does not yet need a moving machine."
                ],
            ),
        ],
        [("Robotics program", "/programs/robotics"), ("Robot Maze Logic", "/projects/robot-maze-logic"), ("Sensors topic", "/topics/sensors")],
    ),
    "how-robots-sense-the-world": article(
        "How Robots Sense the World",
        "Robotics for Kids",
        "A sensor turns one physical signal into values. The program and its author decide what those values mean.",
        (
            "A robot does not see a chair or notice darkness in the broad human sense. Its sensor measures something narrower: distance, reflected light, pressure, motion, temperature, or orientation. Code gives that reading a job in the current task."
        ),
        [
            (
                "Begin with the raw reading",
                [
                    "The number 347 is not yet useful. Which sensor produced it? What scale does it use? What values appear near a window, under a desk, or with an object at arm's length? The reading does not arrive labelled ‘dark’ or ‘too close.’",
                    "Students should watch the values before programming a response. This exposes variation that a polished final behaviour might conceal."
                ],
            ),
            (
                "Make a small table",
                [
                    "Move an object to three distances, press and release a button several times, or compare light readings in two parts of a room. Record what stays stable, what changes, and where the ranges overlap.",
                    "Now the class has evidence about a limited measuring device. It can ask whether a single sample is reliable, whether the environment matters, and what the sensor cannot detect."
                ],
            ),
            (
                "Choose a threshold",
                [
                    "A robot might turn when distance is less than 15. The sensor supplies the measurement; the programmer chooses 15. If the robot reacts too late, the threshold or speed may need changing. If readings jump around the boundary, the code may need several samples or a wider margin.",
                    "Test cases just above and below the threshold. A wobbling result is worth showing because it reveals whether the limitation belongs to the sensor, sampling, environment, or decision rule."
                ],
            ),
            (
                "Expect noise",
                [
                    "Distance readings change with angle and material. Buttons can bounce between states. Light sensors respond to the actual room, including the window someone just opened the blind beside. One perfect number every time would be convenient and suspicious.",
                    "Repeating measurements, comparing ranges, and calibrating in the working environment are early forms of data literacy."
                ],
            ),
            (
                "Close the feedback loop",
                [
                    "A patrol robot measures an obstacle, turns, and checks again. The new reading tells it whether the action helped. That cycle—measure, decide, act, measure again—is feedback.",
                    "This method prepares students for later discussions of computer vision and AI. More advanced sensing still involves measurements, uncertainty, models or thresholds, and human decisions about success.",
                    "A student can narrate the whole loop: the sensor produced this range, the code compared it with that threshold, the motor changed, and the next reading showed whether the turn was enough. If the explanation skips from sensor to intelligent robot, there is probably a decision rule still waiting to be found.",
                ],
            ),
            (
                "Choose the sensor for the question",
                [
                    "Sensor choice also follows the task. A button answers a different question from a light or distance sensor. Adding more sensors does not automatically improve the system; it adds readings, wiring, and cases the program must handle. One well-understood input is a respectable place to begin.",
                    "Those choices should remain visible in the final explanation and test record."
                ],
            ),
        ],
        [("Sensors topic", "/topics/sensors"), ("Sensors lesson", "/lessons/sensors-as-questions"), ("Robot Patrol Challenge", "/projects/robot-patrol-challenge")],
    ),
    "what-is-a-microcontroller": article(
        "What Is a Microcontroller?",
        "Robotics for Kids",
        "A microcontroller is a small computer that reads inputs and controls outputs inside a device.",
        (
            "A laptop is built to do many kinds of work. A microcontroller is smaller and more focused. It runs a program that reads pins or built-in sensors, remembers a little state, and controls lights, sounds, displays, or motors."
        ),
        [
            (
                "One part of the machine",
                [
                    "The controller is usually not the whole project. The battery supplies power, a button or sensor provides input, and an LED or motor produces output. Code on the controller coordinates those pieces.",
                    "This makes input-process-output easy to inspect. Press a button, evaluate a condition, light an LED. Each part has a clear responsibility."
                ],
            ),
            (
                "A micro:bit reaction timer",
                [
                    "A micro:bit includes buttons, an LED display, motion sensing, radio, and connection pins. For a reaction timer, it can wait for a random delay, show a signal, read a button press, calculate elapsed time, and display the result.",
                    "The board is the material; state and measurement are the lesson. The program moves through waiting, ready, pressed too soon, measured, and reset. A simulator can establish the logic. A physical board adds real input and timing."
                ],
            ),
            (
                "Pins, polarity, and other facts of life",
                [
                    "In a screen project, an object reference is usually dependable. Physical work adds loose connections, reversed components, wrong pins, unsuitable power, and parts that simply do not behave as expected.",
                    "Students learn to test in layers. Can the output work by itself? Is the chosen pin correct? Is the component connected in the right direction? Does the complete input rule then work? This separates circuit faults from code faults."
                ],
            ),
            (
                "What it does well",
                [
                    "A microcontroller can repeat a defined cycle very quickly: read an input, update a value, choose an output, and begin again. It can time a reaction, control a signal sequence, or sound an alarm when a threshold is crossed.",
                    "It does not understand whether the alarm rule is sensible or why one reaction time looks unusual. Those judgments belong to the people designing and testing the system."
                ],
            ),
            (
                "Keep the hardware promise accurate",
                [
                    "A public project page can explain a microcontroller activity without promising that a board is included. Some groups may use simulation; some physical projects require a micro:bit; components may be arranged for a particular class. Those details need to be confirmed for the actual group.",
                    "The curriculum underneath remains stable: commands, input, output, conditions, state, timing, and debugging. A microcontroller gives those ideas pins, lights, and the occasional loose wire.",
                ],
            ),
            (
                "Starting state matters",
                [
                    "Students should also know that programs on many microcontrollers begin running as soon as the board powers up. That makes the starting state important. An output left on, a timer carrying the wrong value, or a motor moving before the system is ready can turn a small oversight into very visible behaviour.",
                    "A useful demonstration separates the layers. Show the raw button input, then the state change, then the LED output. If the finished timer misbehaves, those smaller checks give the student somewhere sensible to begin instead of replacing the entire project."
                ],
            ),
        ],
        [("micro:bit Reaction Timer", "/projects/microbit-reaction-timer"), ("Input and Output", "/topics/input-and-output"), ("Robotics program", "/programs/robotics")],
    ),
    "why-robot-projects-teach-real-problem-solving": article(
        "Why Robot Projects Make Good Problems",
        "Robotics for Kids",
        "Robots make students separate code, measurements, physical parts, and assumptions about the world.",
        (
            "A perfectly reasonable program can still drive a robot into a chair. The sensor may vary, a wheel may slip, a connection may fail, or the carefully measured turn may have been tested on a different floor. Robotics gives a problem several layers, all visible in the result."
        ),
        [
            (
                "Turn the mission into tests",
                [
                    "‘Patrol the room’ is a wish, not yet a specification. Students need a starting state, a route, a definition of obstacle, an allowed response, and a stopping rule. Each vague word becomes a question the system can answer.",
                    "That decomposition is engineering at a manageable scale. Before writing more code, the student learns to ask which information is missing."
                ],
            ),
            (
                "One symptom, several causes",
                [
                    "An LED that stays dark may point to output code, state logic, pin choice, component direction, connection, or power. A patrol that turns forever may have a sensor condition, recovery state, or loop exit problem.",
                    "A useful test order narrows the field. Check the output alone. Display the input. Show the current state. Then connect the complete rule. Replacing code and parts at random destroys the evidence."
                ],
            ),
            (
                "Split the system",
                [
                    "If a robot misses an obstacle, display the sensor reading while the motors are off. Test motor movement with known values and no sensor rule. Run the decision logic in simulation with a short list of samples. Each test isolates one relationship.",
                    "Sometimes the decision works and the reading is noisy; sometimes the circuit works and the timing is wrong. Finding the boundary between layers is often the most sophisticated part of the project."
                ],
            ),
            (
                "Reality supplies feedback",
                [
                    "A short turn gives a measurable result. Compare it with the target, change one value, and run the same test again. If the machine works on one surface and fails on another, record that operating limit instead of quietly moving the demonstration.",
                    "The physical world is helpful in this respect. It refuses to behave like a diagram and requires students to say where their rule applies."
                ],
            ),
            (
                "Finish with an honest demonstration",
                [
                    "The student states the goal, shows the input, explains the decision, and observes the output under a known test. One limitation or repaired bug belongs in the account.",
                    "A button-and-buzzer system understood from end to end can teach more than an advanced kit assembled by following pictures. The machine need not look futuristic. It needs to be explainable.",
                ],
            ),
            (
                "Measure before changing",
                [
                    "This kind of work also changes the student's relationship with measurement. ‘It turned too far’ becomes an angle, duration, or distance that can be recorded. ‘The sensor is bad’ becomes a range of readings under named conditions. Better descriptions lead to better tests, and better tests lead to repairs that can be repeated.",
                    "There is room for invention after the core is dependable. Students can choose a patrol route, design the warning signal, or decide how the robot recovers. The constraints give those choices weight because every new behaviour must coexist with the system already working."
                ],
            ),
        ],
        [("Robotics projects", "/projects#robotics-projects"), ("Robot Patrol Logic", "/lessons/robot-patrol-logic"), ("Our Method", "/method")],
    ),
}


BLOG_POSTS.update(
    {
        "what-kids-learn-from-making-games": article(
            "What Kids Learn From Making Games",
            "Coding for Kids",
            "Even a small game brings rules, mathematics, testing, writing, and explanation into one working system.",
            (
                "A chase game looks like entertainment because, with luck, it is entertaining. Under the running and ridiculous noises, the student is coordinating position, input, timing, collision, score, feedback, and restart behaviour. The visible game gives those ideas somewhere to meet."
            ),
            [
                (
                    "Rules have to be exact",
                    [
                        "A student may say that the player wins by reaching safety. The program needs details. Which object counts as safety? How often is contact checked? What happens if the pursuer arrives at the same moment?",
                        "This precision supports the invention. An imagined world becomes playable only when its author decides what the system allows."
                    ],
                ),
                (
                    "Numbers acquire consequences",
                    [
                        "Coordinates place characters, destinations, and hazards. Variables hold score, time, health, fuel, or mood. Random values create variation inside chosen bounds. Distance can change an enemy's speed.",
                        "The mathematics is visible. The wrong sign sends Grandma's Intergalactic Taxi away from its passenger. A score updated every frame becomes absurd very quickly."
                    ],
                ),
                (
                    "The player is part of the design",
                    [
                        "Controls, goals, feedback, and consequences communicate with the player. A hidden hazard may be coded correctly and still feel unfair. A coin that scores twice gives false information. Technical choices determine whether another person can understand the game.",
                        "A second player will press keys in an unexpected order, approach the goal from the wrong side, or restart during a message. The author decides whether the result is a bug, an acceptable rule, or a promising accident."
                    ],
                ),
                (
                    "Testing is a different kind of playing",
                    [
                        "While building, students test controls, edges, collisions, and restart. A good test looks for trouble: Can win and loss happen together? Can an object spawn outside the stage? Can one event score twice?",
                        "Their own successful run is not enough. Peer testing shows whether the rules and visual clues communicate without an explanation whispered over the tester's shoulder."
                    ],
                ),
                (
                    "Finishing teaches scope",
                    [
                        "Children are excellent at imagining enormous games. The useful editorial work is finding a small complete version: one level, reliable movement, a goal, a loss rule, and restart. Extra worlds can wait until this one works.",
                        "Once a version can be shown, the student can compare revisions and explain why a clearer warning, fairer risk, or better reset changed the experience. Authorship becomes visible in those choices, not just in the title screen.",
                    ],
                ),
                (
                    "Words are part of the system",
                    [
                        "Games also make writing matter. Titles, instructions, dialogue, labels, and feedback have to be brief enough to read while playing and clear enough to guide action. A clever message that leaves the player confused is still unclear writing. The student edits words and rules for the same audience.",
                    ],
                ),
                (
                    "Serious systems, strange premises",
                    [
                        "The resulting project may feature a giant pigeon or a lost space chicken. That is fine. The comedy supplies a reason to care whether the collision works; it does not lower the standard for the coordinate system underneath.",
                        "A single playable game can require arithmetic, rules, writing, and attention to another person's choices."
                    ],
                ),
            ],
            [("Scratch program", "/programs/scratch"), ("Project library", "/projects#scratch-projects"), ("Coordinates lesson", "/lessons/coordinates-and-movement")],
        ),
        "roblox-as-a-creative-coding-platform": article(
            "Roblox as a Creative Coding Platform",
            "Coding for Kids",
            "Roblox Studio can connect familiar game ideas to Lua and 3D systems when the curriculum and account safeguards are ready.",
            (
                "Many children know Roblox as players. Studio can change that relationship: instead of entering someone else's world, the student defines objects, properties, events, rules, and behaviour in a small world of their own. Familiarity helps, but it is not the same as knowing how to build."
            ),
            [
                (
                    "The bridge to Lua",
                    [
                        "A student who has used events, variables, conditions, and state in Scratch will meet them again in Lua. The punctuation changes; the questions do not. What starts this function? Which object changes? Where is the score stored? What prevents one coin scoring twice?",
                        "Roblox belongs in a curriculum when it extends those ideas into typed scripts, functions, objects, and 3D coordinates—not as a prize for surviving visual programming."
                    ],
                ),
                (
                    "A map needs systems",
                    [
                        "A detailed landscape can be an impressive piece of modelling without containing much programming. An obby becomes a coding project when checkpoints preserve state, hazards follow clear collision rules, and the difficulty is tested. A coin world needs reusable collection logic and dependable score rules.",
                        "The student should be able to point past the scenery and explain what the world remembers, checks, and changes."
                    ],
                ),
                (
                    "Shared worlds add new questions",
                    [
                        "One variable may be enough for a single-player Scratch score. A multiplayer world raises harder questions: which information belongs to one player, which belongs to the server, and what can another player change? These ideas need a careful sequence.",
                        "The first goal is a dependable small system, not a commercial-scale game. Servers are not impressed by ambition."
                    ],
                ),
                (
                    "Assets have a history",
                    [
                        "Studio makes it easy to import models and scripts. Students need to know what they created, what the platform supplied, and what arrived from elsewhere. An attractive free model can also contain code the student has never read.",
                        "Original work, attribution, and inspection of imported behaviour are part of programming responsibility on a platform built for sharing."
                    ],
                ),
                (
                    "Why the program is listed for later",
                    [
                        "School of Code needs clear decisions about accounts, privacy, publishing, external models, collaboration, and device performance before Roblox classes open. The curriculum must also teach Lua and system design rather than drift into decoration or copied scripts.",
                        "For now, Roblox Studio / Lua is marked Available later. Scratch and Robotics are active first and teach ideas that will transfer when the operating details and course sequence are ready.",
                    ],
                ),
                (
                    "Publishing is a separate decision",
                    [
                        "When the program opens, publishing cannot be treated as an automatic final step. A project can be built and reviewed without making it public. Names, chat, collaboration permissions, and any material borrowed from elsewhere need rules that parents and students can understand before accounts are used.",
                        "The eventual course should therefore be judged by what students can explain and change, not by whether the world resembles a popular Roblox genre. A modest obby with sound state logic is a stronger beginning than a vast copied map with an unknown collection of scripts running underneath it."
                    ],
                ),
            ],
            [("Roblox program", "/programs/roblox"), ("Obby Basics", "/projects/obby-basics"), ("Coin Collector World", "/projects/coin-collector-world")],
        ),
        "what-is-project-based-learning": article(
            "What Is Project-Based Learning?",
            "Project-Based Learning",
            "A useful project makes an idea testable, gives students consequential choices, and ends with something they can explain.",
            (
                "Putting a craft at the end of a lesson does not automatically make the learning project-based. The project has to change the work. Students apply an idea, meet its consequences, make decisions, inspect errors, and produce a version that can be demonstrated."
            ),
            [
                (
                    "Start with an idea",
                    [
                        "Coordinates, state, feedback, or input and output give the build a structure. Without that structure, a project can become a collection of copied tricks: movement blocks with no understanding of position, or a sensor connected without any distinction between measurement and decision.",
                        "A class can name the idea, test it in a small example, and then place it inside a guided build. The project makes the consequences visible."
                    ],
                ),
                (
                    "Guide the core",
                    [
                        "A guided project establishes a reliable beginning: a known start, working movement, collision, state, and restart. Checkpoints keep the student from balancing five new systems at once.",
                        "Guidance should leave room for authorship. Change the movement rule, redraw the map, add another safe area, choose a challenge card, or solve the same requirement differently. At least one decision should have a visible consequence."
                    ],
                ),
                (
                    "Let failures teach",
                    [
                        "Projects reveal misunderstandings that a correct worksheet answer may hide. A loop never stops because its condition never changes. A score rises repeatedly because collision is checked every frame. A robot enters recovery state and cannot leave.",
                        "The instructor helps the student preserve the evidence and find the relevant idea. Replacing the code immediately may finish the object, but it removes the lesson."
                    ],
                ),
                (
                    "Define a finish",
                    [
                        "Polished artwork is not the finish line. The project needs a working core, a known start, tests for success and failure, and an explanation of one decision. A game might need one level, one goal, one hazard, and reliable restart before it needs a soundtrack.",
                        "Reducing scope can protect authorship. Keep one sensor, postpone the second character, or save the bonus level for later. A small complete version produces evidence for the next revision."
                    ],
                ),
                (
                    "Show the work",
                    [
                        "At the end, the student demonstrates the mission, identifies the important systems, shows success and failure, describes a bug, and explains a personal change. One unresolved limit may belong in the account too.",
                        "That conversation tells an instructor or parent more than a screenshot. It also provides the substance for a gallery note or blog entry without requiring public sharing or personal information.",
                    ],
                ),
                (
                    "Projects belong in a sequence",
                    [
                        "Projects also make sequence visible across a course. The first version may establish movement; the next uses conditions for boundaries; a later one introduces state for win and loss. Students meet an idea more than once, under slightly different pressure, rather than completing a single grand assignment and leaving the concept behind.",
                        "This is why the surrounding lessons still matter. A project can motivate a question, but the class gives the question a name, a model, and examples beyond the current theme. Build and explanation take turns."
                    ],
                ),
            ],
            [("Our Method", "/method"), ("Computer Lab", "/computer-lab"), ("Lesson library", "/lessons")],
        ),
        "why-small-groups-work-better-for-coding": article(
            "Why Small Groups Matter in Coding Class",
            "Parent Guides",
            "Small groups let an instructor understand the project in front of each student and give useful help at the right moment.",
            (
                "Three unfinished games can be stuck for three unrelated reasons. One student has confused x and y. Another checks collision only once. The third understands both but has planned six levels with twelve minutes left. Useful help begins by seeing the difference."
            ),
            [
                (
                    "Projects diverge quickly",
                    [
                        "Once students choose characters, map sizes, and rules, their code no longer matches a single answer sheet. ‘Check your movement’ may be too broad to help anyone.",
                        "An instructor who can inspect the actual project might ask the student to predict one key press, display the coordinate, and compare the result. The question stays attached to the system on screen."
                    ],
                ),
                (
                    "Waiting has a limit",
                    [
                        "Being stuck can be productive while a student thinks, tests, and gathers evidence. It becomes dead time when the student has no idea what to inspect and waits too long to ask.",
                        "Small groups shorten the distance between a precise problem and useful guidance. They also make quiet students visible. Silence may mean careful work, or it may mean nothing has changed for ten minutes."
                    ],
                ),
                (
                    "Fast finishers need thought too",
                    [
                        "A student who finishes the core early does not need a random heap of extra features. The next task can deepen the same idea: handle an edge, make state visible, compare two routes, or explain why one rule is more reliable.",
                        "Students can share a topic while working at different depths. The group stays together even when the projects are not identical."
                    ],
                ),
                (
                    "Collaboration needs watching",
                    [
                        "Students can read a test aloud, compare two conditions, and help after trying independently. Explaining a rule often strengthens both people.",
                        "The instructor also has to notice when help turns into taking over the keyboard. Collaboration works when the author remains responsible for the consequential changes."
                    ],
                ),
                (
                    "Timely, then independent",
                    [
                        "The aim is not an adult hovering over every click. A well-timed question can prevent twenty minutes of random edits; a patient pause can let the student discover that the variable never reset. Both choices require attention to the learner and the program.",
                        "School of Code is designed around small groups, though a final published maximum has not been set. The operating principle is clear: the instructor should be able to understand each student's real project, not only deliver the explanation at the front.",
                    ],
                ),
                (
                    "What the group makes possible",
                    [
                        "Small groups also support short demonstrations during class. One student can show a useful test; another can compare a different solution. These moments let students see several ways to express the same idea without requiring every project to return to a common template.",
                        "None of this guarantees that every minute will be quiet or effortless. Programming produces stubborn bugs, lively explanations, and occasional negotiations about whether the pigeon really needs lasers. The advantage is that the teacher can keep those moments connected to the work.",
                        "The result is a teacher who knows when to step in and when to leave the keyboard alone."
                    ],
                ),
            ],
            [("For Parents", "/parents"), ("Our Method", "/method"), ("Contact", "/contact")],
        ),
        "can-kids-learn-ai-safely": article(
            "Can Kids Learn AI Safely?",
            "AI for Kids",
            "A safe AI activity has a narrow purpose, non-personal inputs, adult-reviewed tools, and a serious plan for checking errors.",
            (
                "Children meet systems labelled AI in search, recommendations, games, cameras, and writing tools. A useful lesson gives them questions to ask: What information went in? What did the system produce? How could we test it? What decision still belongs to a person?"
            ),
            [
                (
                    "Begin with a visible pattern",
                    [
                        "Students can build simple guessing rules before using a complex model. They choose a pattern, test new examples, and record where the rule fails. This establishes an important fact early: a plausible guess can be wrong for reasons we can investigate.",
                        "The AI Guessing Game preview uses that approach. Correct and incorrect results matter equally because the work is evaluation, not applause."
                    ],
                ),
                (
                    "Give the activity a boundary",
                    [
                        "A first investigation needs one question, a defined tool, and a way to record mistakes. Students might test whether a fictional chatbot follows three character rules or compare how a classifier handles new examples.",
                        "Open-ended use makes both evaluation and safety harder. A narrow task lets the group decide what evidence counts and when to stop."
                    ],
                ),
                (
                    "Treat privacy as part of the lesson",
                    [
                        "Personal details, private conversations, school records, and identifiable images do not belong in external tools used for a class exercise. Tool choice, accounts, retention, permission, and what is sent to a service require adult review in advance.",
                        "Families should hear the actual activity—not simply the word AI. A guessing experiment, image classifier, and chatbot test have different inputs and risks. Clear names support useful questions and meaningful consent."
                    ],
                ),
                (
                    "Polish proves very little",
                    [
                        "A chatbot can write a confident falsehood. An image system can reproduce stereotypes. A prediction can fail because important examples were absent. Students need to collect these cases, verify claims with suitable sources, and record uncertainty.",
                        "Human judgment remains responsible for what is believed, published, or acted upon. Fluency is a style of output, not a certificate of truth."
                    ],
                ),
                (
                    "Why AI is listed for later",
                    [
                        "School of Code marks AI & Smart Machines Available later. Tool selection, privacy arrangements, classroom boundaries, and the curriculum itself have to be settled before an activity becomes an active offer.",
                        "The aim is careful literacy: students who can state what a system did usefully, show where it failed, protect information, and keep responsibility with people.",
                    ],
                ),
                (
                    "A stop rule belongs in the plan",
                    [
                        "A written activity plan should name the input students will use, the output they will inspect, and the checks they will perform. It should also say what happens if the tool changes, requires an unexpected login, or starts requesting information outside the task. Stopping is a valid technical decision.",
                        "No classroom rule can make an external system perfectly predictable. The practical safeguard is layered: choose a limited service, avoid personal data, supervise use, keep the task narrow, and discuss problematic output rather than quietly discarding it. That gives students a procedure they can understand.",
                        "The same procedure needs review whenever a service changes its terms, retention policy, or classroom access."
                    ],
                ),
            ],
            [("AI program", "/programs/ai"), ("AI Guessing Game", "/projects/ai-guessing-game"), ("For Parents", "/parents")],
        ),
        "ai-is-not-magic-teaching-kids-to-question-it": article(
            "Teaching Kids to Question AI",
            "AI for Kids",
            "A good AI lesson examines what a system produced, what evidence supports it, and which failures repeat.",
            (
                "An AI demonstration is designed to look effortless: enter a prompt, receive text, an image, or a prediction. The missing work is evaluation. A classroom should put that work back on the table and give students a way to investigate the output."
            ),
            [
                (
                    "Use verbs we can test",
                    [
                        "A model predicts, classifies, generates, ranks, or matches patterns. These verbs describe operations we can observe. ‘Thinks,’ ‘understands,’ and ‘wants’ may be convenient figures of speech, but they are poor technical explanations.",
                        "Precise language opens useful questions. What was predicted? From which input? Under what conditions did the classification change?"
                    ],
                ),
                (
                    "Keep the failures",
                    [
                        "A class that shows only successful outputs teaches stagecraft. Better tests ask related questions, change one condition at a time, and save inconsistent or invented answers alongside the useful ones.",
                        "The Confidently Wrong Machine idea makes certainty itself worth examining. Does the answer name a source? Can the claim be checked? Does the same kind of error appear again?"
                    ],
                ),
                (
                    "Make an evidence table",
                    [
                        "Record the input, the output, what was checked, the result, and a failure category. Categories might include invented fact, missing context, inconsistent rule, biased example, or claim that cannot be verified.",
                        "This is firmer than saying an answer sounded intelligent. It also shows that a longer prompt does not repair every problem. Sometimes the tool is unsuitable; sometimes the question lacks information; sometimes another source must settle the matter."
                    ],
                ),
                (
                    "Talk about bias through examples",
                    [
                        "Patterns depend on the examples and labels used to produce them. If important cases are missing or poorly labelled, results can be uneven. Students do not need advanced statistics to compare which examples were tested and which group of cases failed.",
                        "Concrete questions keep bias from becoming a vague warning. What information was absent? Who might be affected by this mistake? Would a different test set expose it?"
                    ],
                ),
                (
                    "Keep a human decision boundary",
                    [
                        "A classroom protocol should say what the tool may support and what a person must verify. Generated possibilities may help with brainstorming. Factual claims require checking. Safety limits for a robot remain human-defined.",
                        "Students should leave able to make a modest, supported claim about what the system did and where it failed. That position takes more work than either awe or blanket rejection, which is precisely why it is worth teaching.",
                    ],
                ),
                (
                    "Test the artifact",
                    [
                        "The same discipline applies to generated images and code. An image can contain odd or stereotyped details; a code suggestion can be insecure, irrelevant, or simply fail to run. Students should inspect the actual artifact, test it in a controlled setting, and avoid publishing material whose origin or accuracy they cannot explain.",
                        "Questioning a system does not require knowing every detail of model training. Children can compare outputs, seek independent evidence, and notice which prompts or examples change the result. Those are honest experiments at an appropriate scale.",
                    ],
                ),
                (
                    "Keep the conclusion narrow",
                    [
                        "A narrow experiment supports a narrow conclusion. Everything beyond it remains a question."
                    ],
                ),
            ],
            [("AI & Smart Machines", "/programs/ai"), ("Chatbot Character Lab", "/projects/chatbot-character-lab"), ("Debugging", "/topics/debugging")],
        ),
        "from-scratch-to-robots-to-ai": article(
            "From Scratch to Robots to AI",
            "Computer Lab Notes",
            "Different tools can deepen the same ideas: events, state, sensing, feedback, testing, and judgment.",
            (
                "Scratch, robotics, Roblox, and AI look like separate subjects on a program list. In a coherent curriculum, ideas travel between them. An event starts behaviour. A variable preserves information. A condition turns that information into a choice. Feedback connects an action to what happened next."
            ),
            [
                (
                    "Scratch puts the structure on screen",
                    [
                        "Students can see event blocks, loops, conditions, variables, and messages. A coordinate change produces motion immediately, and a state bug produces a visible contradiction.",
                        "The result is a complete object that can be changed. Students write rules for a game or story, test those rules, and explain how the pieces work together."
                    ],
                ),
                (
                    "Robotics adds an unruly world",
                    [
                        "The same structures meet buttons, sensors, circuits, motors, and timing. A route uses commands and direction; a patrol adds repeated sensing, decisions, state, and feedback.",
                        "Connections fail and readings vary. Students learn to distinguish a program problem from a hardware problem or a poor assumption about the environment."
                    ],
                ),
                (
                    "Lua changes the notation",
                    [
                        "Roblox Studio can later connect these concepts to typed functions, objects, 3D coordinates, and larger game systems. The blocks disappear, but events and variables survive the journey.",
                        "Text code is useful when it supports a new kind of project. A solid Scratch foundation means the student already has ideas worth expressing in the new syntax."
                    ],
                ),
                (
                    "AI adds uncertain output",
                    [
                        "AI systems may return useful language, images, classifications, or predictions, and they may be wrong. Earlier habits become more important: inspect inputs, test unfamiliar cases, classify failures, and state limits.",
                        "This area also needs explicit privacy rules and human decision boundaries. A fluent result does not remove the need for evidence."
                    ],
                ),
                (
                    "The route can bend",
                    [
                        "This is a web of recurring ideas, not a ladder every student must climb in order. A circuit may clarify events first met in a game. A coordinate game may make a robot map easier to discuss. Someone drawn to hardware may first understand variables through reaction time.",
                        "Scratch and Robotics are active now. Roblox and AI remain later directions until their curriculum and operating arrangements are ready. The point of the map is to show connections, not to hand out badges for reaching the far end.",
                    ],
                ),
                (
                    "Students can stay with one medium",
                    [
                        "Teachers can make the links explicit. Compare a Scratch touching check with a physical distance threshold. Ask where state lives in a pet game and in a traffic light. Contrast a fixed robot rule with a future prediction system. The nouns change, so the recurring logic is easy to miss unless someone points to it.",
                        "Students may also stay with one medium for a long time. A richer Scratch game can require functions, messaging, lists, and careful state. A simple circuit can reward several rounds of measurement and redesign. Progress means better reasoning and stronger projects, not faster movement through the program menu.",
                    ],
                ),
                (
                    "Long visits matter",
                    [
                        "A curriculum map should allow those long visits; fluency grows through revision, not tourism."
                    ],
                ),
            ],
            [("Programs", "/programs"), ("Topic library", "/topics"), ("Computer Lab", "/computer-lab")],
        ),
        "the-future-computer-lab-games-robots-and-smart-machines": article(
            "A Computer Lab for Games, Robots, and Smart Machines",
            "Computer Lab Notes",
            "The Lab gives students time and guidance to change, test, repair, and finish projects across different materials.",
            (
                "A computer lab can mean a row of identical desktops, or a room full of fashionable equipment waiting to be admired. School of Code uses the name for working time. The school teaches a planned sequence; the Lab gives students room to take those ideas further in projects."
            ),
            [
                (
                    "One idea, several projects",
                    [
                        "A lesson on coordinates introduces x and y, starting positions, prediction, and boundaries. Escape from the Giant Pigeon uses those ideas in a guided game. Grandma's Intergalactic Taxi turns them into destinations and routes. Astro-Chicken Rescue tracks several moving objects.",
                        "The themes change. The position model remains available for the student to recognize and reuse."
                    ],
                ),
                (
                    "Choices need useful limits",
                    [
                        "Lab students might select a challenge card, theme, implementation, or improvement. The instructor helps keep the project small enough to finish and asks for evidence when a fix is proposed.",
                        "There is room for strange ideas. There is also a deadline, a test plan, and a saved version that still works."
                    ],
                ),
                (
                    "Tools should earn shelf space",
                    [
                        "A condition can control quiz feedback, a traffic-light transition, or a robot's obstacle response. A variable can hold score, reaction time, or patrol state. A microcontroller makes timing physical; a sensor exposes measurement; a robot reveals the limits of feedback.",
                        "The value comes from these connections, not the number of devices in the room. Equipment belongs when it gives an idea a useful form and students can explain what it changed."
                    ],
                ),
                (
                    "Arrange the room around work",
                    [
                        "Some tasks need a screen. Others need a paper grid, a safe circuit surface, components, or enough floor to test movement. There should be places to plan, build, demonstrate, and store unfinished work without losing half of it.",
                        "Clear handling rules, privacy boundaries, and time to reset the workspace make experimentation sustainable. Small groups let the instructor understand the actual project when a peculiar idea begins expanding in every direction."
                    ],
                ),
                (
                    "What progress looks like",
                    [
                        "The Lab has a project, checkpoint, test, repair, or demonstration in view. It is not a drop-in gaming room or an excuse for uncontrolled browsing. Students should leave knowing what changed and what they will try next.",
                        "Growth should show up in finished versions, better tests, clearer explanations, and connections across materials. New machines are welcome when they strengthen that work. Otherwise, they can remain perfectly respectable objects on someone else's shelf.",
                    ],
                ),
                (
                    "Continuity matters",
                    [
                        "A Lab session can therefore look quieter than a product showcase. One student may be tracing a route on paper, another checking a variable on screen, and another testing an LED before reconnecting the sensor. The common feature is a question each student can state and a result that moves the project forward.",
                        "Projects also need continuity. File names, parts trays, brief notes, and a known next step save the beginning of the following session from becoming an archaeological dig. Finishing includes leaving the work in a condition that can be resumed."
                    ],
                ),
            ],
            [("Computer Lab", "/computer-lab"), ("Coordinates topic", "/topics/coordinates"), ("Project library", "/projects")],
        ),
    }
)


BLOG_ORDER = [
    "is-coding-class-just-more-screen-time",
    "what-age-should-kids-start-programming",
    "why-scratch-is-a-great-first-programming-language",
    "why-debugging-is-good-for-kids",
    "robotics-for-kids-where-to-start",
    "how-robots-sense-the-world",
    "what-is-a-microcontroller",
    "why-robot-projects-teach-real-problem-solving",
    "what-kids-learn-from-making-games",
    "roblox-as-a-creative-coding-platform",
    "what-is-project-based-learning",
    "why-small-groups-work-better-for-coding",
    "can-kids-learn-ai-safely",
    "ai-is-not-magic-teaching-kids-to-question-it",
    "from-scratch-to-robots-to-ai",
    "the-future-computer-lab-games-robots-and-smart-machines",
]


BLOG_CATEGORIES = [
    "Coding for Kids",
    "Robotics for Kids",
    "AI for Kids",
    "Parent Guides",
    "Project-Based Learning",
    "Computer Lab Notes",
    "Calgary STEM Activities",
]


for post_slug, post in BLOG_POSTS.items():
    post["slug"] = post_slug
    post["url"] = f"/blog/{post_slug}"
    post["meta_description"] = post["description"]
    post.setdefault("categories", [post["category"]])


BLOG_POSTS["what-age-should-kids-start-programming"]["categories"].extend(
    ["Parent Guides", "Calgary STEM Activities"]
)
BLOG_POSTS["why-small-groups-work-better-for-coding"]["categories"].extend(
    ["Parent Guides", "Calgary STEM Activities"]
)
BLOG_POSTS["the-future-computer-lab-games-robots-and-smart-machines"]["categories"].extend(
    ["Project-Based Learning", "Calgary STEM Activities"]
)
