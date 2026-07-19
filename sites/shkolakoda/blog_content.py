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
        "The useful distinction is not screen versus no screen. It is passive consumption versus active construction, testing, and explanation.",
        (
            "Parents are right to ask what another hour at a computer actually contains. A child can spend an hour "
            "watching an endless feed, or spend an hour building a game, predicting a movement, finding a collision bug, "
            "and explaining why a score changed twice. Both activities use a screen. They are not the same kind of work."
        ),
        [
            (
                "Look at the verbs",
                [
                    "A useful coding class can be described with observable verbs: build, test, debug, change, explain, and improve. The student makes decisions that alter a system. When Escape from the Giant Pigeon starts in the wrong corner, the student inspects x and y values. When win and loss happen together, the student decides which state has priority. The screen is showing the material under construction.",
                    "Passive screen time usually asks very little of the viewer between one item and the next. Project work creates resistance. The program does not care that the student meant to move upward; it changes the axis specified in code. That resistance is educational because it requires a prediction, evidence, and revision."
                ],
            ),
            (
                "What a parent should be able to observe",
                [
                    "After class, a student should have something specific to show. It may be a small game, a robot route, a reaction timer, or a state diagram. More important, the student should be able to answer concrete questions: What starts the program? What number controls left and right? What went wrong? Which rule did you change?",
                    "A finished project is not evidence that every line was written independently or that every concept is mastered. It is evidence that the class had a visible object around which understanding can be discussed. The demonstration makes vague claims about creativity unnecessary."
                ],
            ),
            (
                "Screens still need boundaries",
                [
                    "Calling an activity creative does not make unlimited device use harmless. Classes should have a beginning, a task, checkpoints, and an ending. Students should take visual breaks, talk with people, draw plans on paper when useful, and leave the project in a known saved state. A Computer Lab should not become an excuse for random gaming or unstructured browsing.",
                    "The School of Code distinction is simple: classes follow a planned learning path, while Computer Lab time provides guided project work. In both cases, the device serves the project. The project does not serve the device."
                ],
            ),
            (
                "Ask a better question",
                [
                    "Instead of asking only how many minutes involved a screen, ask what the child was doing during those minutes. Did the student make choices, encounter difficulty, inspect evidence, explain a system, and finish a version that can be demonstrated? If the answer is no, the activity may indeed be only more screen time.",
                    "If the answer is yes, the computer is functioning more like a workshop bench, notebook, stage, and test instrument at once. That does not eliminate the need for limits. It does explain why active programming can belong in a balanced education."
                ],
            ),
        ],
        [("For Parents", "/parents"), ("Computer Lab", "/computer-lab"), ("Escape from the Giant Pigeon", "/projects/escape-from-the-giant-pigeon")],
    ),
    "what-age-should-kids-start-programming": article(
        "What Age Should Kids Start Programming?",
        "Coding for Kids",
        "Readiness depends less on a birthday than on the task, the support, and whether the child can work through a small problem.",
        (
            "There is no single correct age at which programming suddenly becomes appropriate. A young child may enjoy "
            "sequencing commands with strong support, while an older beginner may prefer to understand the purpose before "
            "touching the editor. The practical question is not 'Is my child old enough for coding?' but 'What kind of coding work fits this child now?'"
        ),
        [
            (
                "Readiness is visible in behaviour",
                [
                    "A beginner does not need to type quickly, know algebra, or arrive with technical vocabulary. Useful signs are more ordinary: willingness to follow a short sequence, interest in making something happen, ability to compare an expected result with an actual one, and enough patience to try a second version.",
                    "These abilities are not fixed traits. A good class supports them with small steps and visible outcomes. The first project should be narrow enough that the student can reach a working version before attention is exhausted."
                ],
            ),
            (
                "Choose the representation carefully",
                [
                    "Scratch reduces the burden of spelling and punctuation while preserving events, loops, conditions, variables, messages, and state. That makes it useful for beginners who are ready to reason about systems but would be slowed down by typing every symbol correctly. It is not a toy version of programming; it is a visual representation of real programming structures.",
                    "Robotics can begin without an advanced robot. Paper routes, grid simulations, buttons, LEDs, and small microcontroller activities can make commands and input-output relationships concrete. The representation should reveal the idea rather than bury it beneath setup."
                ],
            ),
            (
                "Challenge depth can change",
                [
                    "Two students can work on the same project at different depths. One may build reliable four-direction movement. Another may add boundary handling, a second stage, or a distance-based pursuer. The common topic remains coordinates; the challenge changes.",
                    "This is why narrow age labels can be misleading before a program's operating details are finalized. Group fit also depends on reading comfort, independence, previous experience, and whether the student enjoys explaining a problem aloud."
                ],
            ),
            (
                "How to decide",
                [
                    "Ask what the child likes to make, not only what software the child recognizes. A student interested in stories may enjoy interactive scenes. A child who likes systems may prefer a traffic light or robot maze. A game enthusiast may become engaged when asked to change the rules instead of merely playing them.",
                    "The sensible next step is a conversation about fit. School of Code does not publish a universal starting age because exact groups and schedules are still being prepared. The goal is a starting task with meaningful difficulty: neither automatic nor overwhelming."
                ],
            ),
        ],
        [("Scratch program", "/programs/scratch"), ("Robotics program", "/programs/robotics"), ("Contact", "/contact")],
    ),
    "why-scratch-is-a-great-first-programming-language": article(
        "Why Scratch Is a Great First Programming Language",
        "Coding for Kids",
        "Scratch makes program structure visible so beginners can spend more attention on events, rules, state, and debugging.",
        (
            "Scratch is often described as easy because its blocks fit together. That description misses its real value. "
            "Scratch is useful because it makes the structure of a program inspectable. Students can see which event starts a script, "
            "which blocks repeat, where a condition branches, and which variable changes."
        ),
        [
            (
                "It removes the wrong difficulty first",
                [
                    "Text syntax matters, but it is not the first idea most beginners need. A missing bracket can stop a typed program before a student has a chance to think about movement or game state. Scratch reduces syntax errors while keeping logical errors alive. A sprite can still move in the wrong direction, score twice, or remain stuck in CAUGHT state.",
                    "Those logical errors are valuable. They concern the system the student intended to build. The editor lets the class discuss coordinates, loops, collision, and state before typing accuracy dominates the lesson."
                ],
            ),
            (
                "It supports complete projects",
                [
                    "Scratch combines code, simple drawing, sound, input, and animation. A student can finish a small game within a lesson and still encounter authentic design decisions. In Escape from the Giant Pigeon, the player needs a known start, movement controls, a pursuer, safe zones, collision checks, win and loss states, and restart logic.",
                    "A finished project gives the student a reason to explain each concept. Coordinates are no longer an isolated worksheet; they determine whether the player can escape. Conditions decide whether contact means safety or disaster."
                ],
            ),
            (
                "It scales by changing the system",
                [
                    "A beginner can move a sprite with four keys. A more experienced student can add acceleration, screen wrapping, state-based controls, or multiple maps. The visual language remains familiar while the relationships become deeper.",
                    "Scratch also makes modification inviting. Students can draw original characters, change rules, and test strange premises. Authorship matters: a program is a text, and the student should make consequential choices rather than only reproduce the instructor's version."
                ],
            ),
            (
                "It is a beginning, not a cage",
                [
                    "Visual programming should connect forward. Events become event handlers in other environments. Variables remain variables. Conditions, functions, messages, and state return in Lua, Python, web programming, robotics, and game engines.",
                    "The transition works best when students know the concepts under the blocks. If they can explain why a loop stops and how a state resets, text-based syntax becomes a new way to express known ideas rather than a completely new universe."
                ],
            ),
        ],
        [("Scratch & Game Design", "/programs/scratch"), ("Topic library", "/topics"), ("Project library", "/projects#scratch-projects")],
    ),
    "why-debugging-is-good-for-kids": article(
        "Why Debugging Is Good for Kids",
        "Project-Based Learning",
        "Debugging replaces vague frustration with a method: describe, inspect, predict, test, and explain.",
        (
            "A bug creates a useful disagreement. The student believes one thing should happen; the system does something else. "
            "That difference can lead to random clicking, or it can become evidence. Teaching debugging means teaching children how to turn surprise into a testable question."
        ),
        [
            (
                "A bug is not a verdict",
                [
                    "When a game fails, children often read the result personally: I am bad at this, or the computer hates me. A debugging routine changes the language. What did we expect? What did we observe? Can we make it happen again? Which value or state would tell us more?",
                    "The bug becomes a clue about the program, not a judgment about the programmer. This does not make difficulty disappear. It gives difficulty a structure."
                ],
            ),
            (
                "Controlled tests beat random repairs",
                [
                    "Suppose a player sometimes wins and loses at once. Adding waits in three scripts may hide the symptom, but it does not explain the cause. A better test displays the game state, reproduces simultaneous contact, and identifies which condition runs first.",
                    "Changing one relevant thing preserves information. If the test result changes, the student has evidence. If it does not, the failed hypothesis is still useful because it removes one possible cause."
                ],
            ),
            (
                "Debugging grows transferable habits",
                [
                    "The same habits appear outside programming. A circuit does not light: first verify the power and output, then inspect one connection. A robot turns too far: measure the result, compare it with the goal, and adjust. A written argument seems weak: identify the claim that does not follow from the evidence.",
                    "Programming gives immediate feedback, which makes these habits visible. The system runs the student's actual instructions, including the assumptions the student did not notice."
                ],
            ),
            (
                "What adults should do",
                [
                    "Helping is not the same as taking the keyboard. An adult can ask for the expected result, narrow the test, point toward a relevant value, or suggest temporarily disabling one script. The student should still make the consequential change and explain why it worked.",
                    "The strongest demonstration is not a flawless project. It is a student who can show one bug, reproduce it, describe the evidence, and explain the repair. That is intellectual independence in a small, practical form."
                ],
            ),
        ],
        [("Debugging topic", "/topics/debugging"), ("Debugging lesson", "/lessons/debugging-clues"), ("Our Method", "/method")],
    ),
    "robotics-for-kids-where-to-start": article(
        "Robotics for Kids: Where to Start",
        "Robotics for Kids",
        "Robotics begins with commands, inputs, outputs, and feedback—not with buying the most advanced robot.",
        (
            "The word robotics can create an expensive picture: autonomous machines, complex kits, and a table covered in parts. "
            "Those tools can be useful later, but the educational starting point is simpler. A robot is a system that can receive information, make a rule-based decision, and produce an action."
        ),
        [
            (
                "Start with Sense, Decide, Act",
                [
                    "The model gives students three questions. What information enters the system? What rule decides what that information means? What visible or physical action follows? A button-buzzer alarm fits the model. So does a simulated robot avoiding a wall.",
                    "Separating the three parts prevents magical explanations. A sensor does not decide; it measures. A motor does not know the goal; it produces output. The program connects measurement, decision, and action."
                ],
            ),
            (
                "Use paper and simulation when they reveal the idea",
                [
                    "Robot Maze Logic can begin on a grid. Students define forward and turn commands, record a starting direction, predict a route, and trace one command at a time. This teaches decomposition, state, and debugging without loose wires competing for attention.",
                    "Simulation is not a lesser activity when the learning goal is logic. Physical hardware should enter when its friction matters: connections fail, motors drift, sensors vary, and the real floor refuses to match the perfect diagram."
                ],
            ),
            (
                "Add simple electronics deliberately",
                [
                    "LEDs, buttons, buzzers, and microcontrollers can make input and output tangible. A traffic light teaches named states and safe sequence order. A reaction timer teaches measurement, random delay, state, and fair testing.",
                    "Hardware requirements should be honest. Some projects are simulation-friendly; some have optional physical versions; a physical micro:bit timer requires a micro:bit. A public project page should not imply equipment is included before group arrangements are confirmed."
                ],
            ),
            (
                "Build toward autonomy slowly",
                [
                    "Autonomy combines commands, loops, sensing, conditions, state, and feedback. A machine that follows a fixed route is not autonomous merely because nobody is touching it. A responsive patrol must inspect changing information and choose from defined responses.",
                    "Students should understand each layer before combining them. The long-term direction may include richer robots, but the first goal is more durable: a child who can explain what the system senses, decides, and does."
                ],
            ),
        ],
        [("Robotics program", "/programs/robotics"), ("Robot Maze Logic", "/projects/robot-maze-logic"), ("Sensors topic", "/topics/sensors")],
    ),
    "how-robots-sense-the-world": article(
        "How Robots Sense the World",
        "Robotics for Kids",
        "Sensors do not give robots human understanding. They turn selected physical signals into values a program can inspect.",
        (
            "A robot does not see a chair, feel danger, or notice darkness in the broad human sense. A sensor measures a limited signal: "
            "distance, reflected light, pressure, motion, temperature, orientation, or another quantity. Code then decides what a reading should mean for the current task."
        ),
        [
            (
                "Measurement comes before meaning",
                [
                    "A value such as 347 is useless without context. Which sensor produced it? What unit or scale does it use? What range appears in this room? A light sensor may report a different number near a window than under a desk, but neither value contains the word dark.",
                    "Students should inspect raw readings before building decisions. That step makes the measurement visible and exposes variation that a polished final behaviour might hide."
                ],
            ),
            (
                "Thresholds are design decisions",
                [
                    "A simple robot may turn when distance is less than 15. The sensor supplies a measurement; the programmer chooses 15 as a threshold. If the robot reacts too late, the threshold or movement may need revision. If readings jump around 15, the system may need several samples or a wider boundary.",
                    "This distinction matters because data never explains itself. Human choices determine which signal to collect, which values matter, and what action is acceptable."
                ],
            ),
            (
                "Noise and limits are part of the lesson",
                [
                    "Real readings change. A distance sensor can be affected by angle or material. A button can bounce between states. A light sensor responds to the environment. Students should not expect one perfect number every time.",
                    "Instead, they can repeat measurements, compare ranges, calibrate in the actual setting, and design behaviour that remains stable near a boundary. These are early forms of data literacy."
                ],
            ),
            (
                "From sensing to feedback",
                [
                    "Sensing becomes powerful when the system acts, checks the result, and adjusts. A patrol robot sees an obstacle, turns, then checks again rather than assuming the turn solved the problem. That repeated loop is feedback.",
                    "The child should be able to narrate it: the robot measured this, the condition compared it with that threshold, the output changed, and the next measurement told us whether the correction helped."
                ],
            ),
        ],
        [("Sensors topic", "/topics/sensors"), ("Sensors lesson", "/lessons/sensors-as-questions"), ("Robot Patrol Challenge", "/projects/robot-patrol-challenge")],
    ),
    "what-is-a-microcontroller": article(
        "What Is a Microcontroller?",
        "Robotics for Kids",
        "A microcontroller is a small programmable computer built to read inputs and control outputs inside a larger system.",
        (
            "A laptop is a general-purpose computer with a screen, storage, and an operating system. A microcontroller is smaller and narrower. "
            "It runs a program that reads pins or built-in sensors, keeps a little state, and controls outputs such as lights, sound, displays, or motors."
        ),
        [
            (
                "A computer inside the project",
                [
                    "The microcontroller is usually not the whole robot or device. It is one component inside the system. The button, sensor, battery, LED, and motor each have separate roles. Code running on the controller coordinates them.",
                    "This is why microcontroller projects are good for input-process-output thinking. A button provides input, a condition interprets it, and an LED provides output. Nothing needs to be described as magic."
                ],
            ),
            (
                "The micro:bit example",
                [
                    "A micro:bit includes buttons, an LED display, motion sensing, radio capability, and connection pins. A reaction timer can wait for a random delay, show a signal, read a button press, calculate elapsed time, and display the result.",
                    "The interesting lesson is not the brand of board. It is state and measurement: waiting, ready, pressed too soon, measured, and reset. A simulator can support the logic, while a physical board adds the behaviour of real input."
                ],
            ),
            (
                "Why wiring changes the work",
                [
                    "In screen projects, an object reference is usually reliable. In physical projects, a loose connection, reversed component, wrong pin, or unsuitable power source can prevent output. Students must distinguish code problems from circuit problems.",
                    "That friction is educational when introduced safely and at the right time. It teaches systematic checking: verify the output alone, inspect connections, confirm the selected pin, then test the complete rule."
                ],
            ),
            (
                "Keep the hardware claim honest",
                [
                    "A project page can explain a microcontroller activity without promising that hardware is currently included. Some classes may use simulation, some may require a micro:bit, and some components may be arranged by the teacher for a specific group.",
                    "The educational pathway remains stable: learn commands, input, output, conditions, state, timing, and debugging. Hardware is a material for those ideas, not a substitute for them."
                ],
            ),
        ],
        [("micro:bit Reaction Timer", "/projects/microbit-reaction-timer"), ("Input and Output", "/topics/input-and-output"), ("Robotics program", "/programs/robotics")],
    ),
    "why-robot-projects-teach-real-problem-solving": article(
        "Why Robot Projects Teach Real Problem-Solving",
        "Robotics for Kids",
        "Robot projects force students to separate goals, commands, measurements, physical limits, and evidence.",
        (
            "A screen program can be perfectly logical and still produce the wrong visible result. A robot adds another layer: the code may be correct, "
            "but a sensor may vary, a wheel may slip, or a connection may fail. That makes robotics difficult. It also makes the problem-solving unusually concrete."
        ),
        [
            (
                "The goal must become testable",
                [
                    "'Patrol the room' is not yet a program. Students must define a route, a starting state, what counts as an obstacle, which response is allowed, and when the patrol should stop. Vague intention becomes a collection of testable systems.",
                    "This decomposition is real engineering work at an accessible scale. The student learns to ask what information is missing before adding code."
                ],
            ),
            (
                "Several kinds of failure can look the same",
                [
                    "If an LED stays dark, the cause may be output code, state logic, a pin choice, component direction, connection, or power. If a simulated patrol turns forever, the cause may be a sensor condition, recovery state, or loop exit.",
                    "Students need a test order. Can the output work alone? Can the input be read? Is the current state visible? Does the complete rule connect them? The sequence prevents random replacement of parts and code."
                ],
            ),
            (
                "Reality creates feedback",
                [
                    "A robot that turns too little provides evidence. Students can measure the result, compare it with the target, change one value, and test again. The physical world makes assumptions visible because it refuses to behave like a perfect diagram.",
                    "Feedback also teaches humility. A system may work on one floor and fail on another. A threshold may work in one lighting condition and fail near a window. The correct response is not to overstate success but to describe the operating limits."
                ],
            ),
            (
                "The demonstration completes the cycle",
                [
                    "A finished robot project should be demonstrated under a known test. The student states the goal, shows the input, explains the decision, observes the output, and discusses one limitation or bug.",
                    "That explanation distinguishes building from assembling. The educational value does not depend on the machine looking advanced. A simple button-buzzer system understood deeply can teach more than an impressive kit whose behaviour remains opaque."
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
            "A game project can make mathematics, logic, writing, testing, and explanation visible inside one playable system.",
            (
                "A finished game is easy to underestimate because the result looks like entertainment. Underneath a small chase, quiz, or platform game, "
                "the student may be coordinating position, input, timing, state, collision, score, feedback, and restart behaviour. The visible fun gives the hidden ideas somewhere to work together."
            ),
            [
                (
                    "Games make rules unavoidable",
                    [
                        "A student can say that the player wins by reaching safety, but the program needs a precise rule. Which object or region counts as safety? How often is contact checked? What if the player touches the pursuer at the same moment? Designing a game turns casual rules into conditions and state transitions.",
                        "This precision is not separate from creativity. It is how an imagined world becomes playable by another person. The author must decide what the system allows and communicate those decisions through behaviour."
                    ],
                ),
                (
                    "Mathematics becomes movement",
                    [
                        "Coordinates describe where characters, targets, and hazards are. Variables hold score, time, health, fuel, or mood. Random values create variation within chosen boundaries. Distance can affect speed or route decisions.",
                        "The mathematics remains accessible because students can see the result. Changing x by the wrong sign sends a taxi away from its passenger. A score that updates every frame becomes obviously unreasonable. The project gives numbers consequences."
                    ],
                ),
                (
                    "Testing becomes part of authorship",
                    [
                        "Playing a game while building it is not the same as casual play. The student tests controls, edges, collisions, restart, and strange combinations. A useful test tries to break an assumption: Can win and loss happen together? Can a falling object appear outside the stage? Can one coin score twice?",
                        "Students also learn that their own successful run is not enough. Another player may press keys in a different order or misunderstand a visual clue. Demonstration and peer testing reveal whether the rules are actually communicated."
                    ],
                ),
                (
                    "Finishing teaches scope",
                    [
                        "Children often imagine a huge game. The educational task is to find a small complete version: one level, reliable controls, a goal, a loss rule, and restart. That version can be shown, explained, and improved.",
                        "A finished small project beats a perfect unfinished one because completion creates evidence. The student can identify which systems work, which compromise was chosen, and which feature belongs in a later version."
                    ],
                ),
            ],
            [("Scratch program", "/programs/scratch"), ("Project library", "/projects#scratch-projects"), ("Coordinates lesson", "/lessons/coordinates-and-movement")],
        ),
        "roblox-as-a-creative-coding-platform": article(
            "Roblox as a Creative Coding Platform",
            "Coding for Kids",
            "Roblox Studio can provide a meaningful bridge to Lua and 3D systems, but familiarity with the platform is not the same as learning to program.",
            (
                "Many children arrive already knowing Roblox as players. That familiarity can become motivation, but a coding class must change the relationship. "
                "The student should move from consuming worlds to defining objects, properties, events, rules, score, and behaviour in an original small project."
            ),
            [
                (
                    "The useful bridge to text code",
                    [
                        "A student who understands events, variables, conditions, and state in Scratch can meet those ideas again in Lua. The syntax is different, but the questions remain recognizable: What starts this function? Which object changes? Where is score stored? What prevents one coin from scoring twice?",
                        "This continuity matters. Roblox should not be presented as an unrelated reward after visual programming. It is one environment where known ideas can grow into typed scripts and larger object systems."
                    ],
                ),
                (
                    "World-building needs system design",
                    [
                        "A detailed 3D map is not automatically a programming project. An Obby Basics project becomes educational when checkpoints preserve state, hazards use clear collision rules, and difficulty is tested for fairness. A Coin Collector World needs reusable collection logic, score rules, and a clear distinction between display and stored state.",
                        "The environment also raises responsibility questions. Students should understand scripts inside models before using them, prefer original work, and avoid treating a large library of copied assets as authorship."
                    ],
                ),
                (
                    "Multiplayer changes assumptions",
                    [
                        "In a single-player Scratch game, one score variable may be enough. In a shared world, students must begin asking which information belongs to one player, which belongs to the server, and what other players can affect. These concepts should be introduced gradually and honestly.",
                        "The goal is not to promise a commercial-quality game. It is to make one small system dependable and explainable before adding scale."
                    ],
                ),
                (
                    "Why School of Code marks it later",
                    [
                        "Roblox Studio / Lua belongs in the School of Code direction, but it is marked Available later. A responsible program needs account and privacy decisions, a clear curriculum bridge, tested project scope, and current scheduling before it is offered.",
                        "The preview pages explain future learning value without pretending instructions or classes are ready now. Scratch and Robotics remain the active first programs."
                    ],
                ),
            ],
            [("Roblox program", "/programs/roblox"), ("Obby Basics", "/projects/obby-basics"), ("Coin Collector World", "/projects/coin-collector-world")],
        ),
        "what-is-project-based-learning": article(
            "What Is Project-Based Learning?",
            "Project-Based Learning",
            "A project is not decoration after a lesson. It is a system where the lesson's ideas become testable, revisable, and explainable.",
            (
                "Project-based learning is sometimes reduced to making something at the end of a unit. That is not enough. A useful project changes the learning process: "
                "students must apply an idea, encounter consequences, make decisions, inspect errors, and produce a version they can demonstrate."
            ),
            [
                (
                    "The project needs a conceptual skeleton",
                    [
                        "Theory is the skeleton. Without it, a project can become a collection of copied tricks. A student may assemble movement blocks without understanding coordinates, or connect a sensor without distinguishing measurement from decision.",
                        "The class should name the idea first, test it in a small form, and then place it inside a guided build. The project gives the concept a body, but the concept keeps the project understandable."
                    ],
                ),
                (
                    "Guidance and authorship must coexist",
                    [
                        "A guided project can establish a reliable core: known start, movement, collision, state, and restart. If every visual choice and rule is prescribed, however, the student has assembled the teacher's text rather than authored a program.",
                        "Meaningful choices can be small. Change the movement rule, add a second safe zone, redesign the map, choose a challenge card, or explain a different implementation. The student should make at least one decision with visible consequences."
                    ],
                ),
                (
                    "Failure produces curriculum",
                    [
                        "Projects expose misconceptions that an explanation alone may not reveal. A loop never stops because its condition never changes. A game score increases repeatedly because collision is checked every frame. A patrol enters recovery mode and never leaves.",
                        "These are not interruptions to learning. They are where loops, state, and feedback become real. The instructor helps preserve the evidence rather than immediately replacing the student's code."
                    ],
                ),
                (
                    "Demonstration matters",
                    [
                        "A project ends with explanation, not merely with a file. The student shows the mission, names the important systems, demonstrates success and failure, describes one bug, and identifies a personal modification.",
                        "That final account makes learning visible to the student, instructor, and parent. It also creates the beginning of a gallery or blog entry without requiring public sharing or personal information."
                    ],
                ),
            ],
            [("Our Method", "/method"), ("Computer Lab", "/computer-lab"), ("Lesson library", "/lessons")],
        ),
        "why-small-groups-work-better-for-coding": article(
            "Why Small Groups Work Better for Coding",
            "Parent Guides",
            "The important advantage is not quietness. It is the instructor's ability to understand each student's actual system and ask the next useful question.",
            (
                "Two projects can look equally unfinished while failing for completely different reasons. One student has confused x and y. Another has a collision rule running only once. "
                "A third understands both but is attempting a feature too large for the remaining time. Coding support depends on seeing the difference."
            ),
            [
                (
                    "Projects are not identical worksheets",
                    [
                        "Once students make choices, projects diverge. Sprites have different sizes, maps have different boundaries, and students organize scripts differently. A generic instruction such as 'check your movement' may be too broad to help.",
                        "In a small group, the instructor can ask the student to predict one key, inspect the relevant coordinate, and compare the result. The help stays attached to the student's actual work."
                    ],
                ),
                (
                    "Waiting time matters",
                    [
                        "Getting stuck is valuable when the student has time to think and a path toward evidence. It becomes unproductive when a student waits too long without knowing what to inspect. Small groups reduce the delay between a precise question and useful guidance.",
                        "They also let the instructor notice students who do not ask. A quiet student may be carefully testing, or may have stopped making progress ten minutes ago. Those situations need different responses."
                    ],
                ),
                (
                    "Advanced students need attention too",
                    [
                        "A student who finishes the core quickly should not receive a random pile of extra features. The next challenge should deepen the same idea: handle a boundary, make state explicit, compare two algorithms, or explain why one implementation is more reliable.",
                        "Small-group teaching makes it easier to select meaningful difficulty without turning the class into separate private lessons. Students can share a topic while working at different project depths."
                    ],
                ),
                (
                    "Collaboration stays accountable",
                    [
                        "Students can help one another after trying independently. Explaining a condition or reading a test aloud can strengthen both students. The instructor can also see when collaboration becomes one student taking over another's keyboard.",
                        "School of Code is designed around small groups, but a final published maximum has not been set. The principle comes first: the instructor should be able to understand the actual project, not only deliver the front-of-room explanation."
                    ],
                ),
            ],
            [("For Parents", "/parents"), ("Our Method", "/method"), ("Contact", "/contact")],
        ),
        "can-kids-learn-ai-safely": article(
            "Can Kids Learn AI Safely?",
            "AI for Kids",
            "Yes, if the learning emphasizes limits, privacy, testing, and human responsibility rather than treating generated output as authority.",
            (
                "Children already encounter systems described as AI in search, recommendations, games, cameras, and writing tools. Avoiding every conversation does not make those systems disappear. "
                "A safe educational approach gives students practical questions: What information went in? What pattern produced the output? How could we test it? What should a person still decide?"
            ),
            [
                (
                    "Start with transparent patterns",
                    [
                        "Before using a complex model, students can build simple guessing rules and test them with new examples. This separates pattern matching from understanding. A system can produce a plausible guess and still be wrong for an explainable reason.",
                        "The AI Guessing Game preview is built around evaluation: record correct and incorrect results, classify errors, and compare confidence with evidence. The point is not to marvel at accuracy."
                    ],
                ),
                (
                    "Privacy is part of the technical lesson",
                    [
                        "Students should not place personal details, private conversations, school records, or identifiable information into external tools. Account setup, tool choice, retention, and permission need adult review before a class uses any service.",
                        "A public project can explain these principles without pretending that a particular AI tool or account is currently approved. School of Code marks AI & Smart Machines Available later for exactly this reason: the curriculum and operating setup both matter."
                    ],
                ),
                (
                    "Fluent language is not evidence",
                    [
                        "A chatbot can state an incorrect claim in a polished voice. An image system can reproduce stereotypes. A prediction can reflect missing or unbalanced examples. Students need to see failures, not only impressive demonstrations.",
                        "Safe learning asks children to verify claims with appropriate sources, identify uncertainty, and record when a tool invents details. Human judgment remains responsible for what is believed, published, or acted upon."
                    ],
                ),
                (
                    "Set a narrow purpose",
                    [
                        "An AI activity should have a bounded educational question: compare prompts, test consistency, classify errors, inspect a pattern, or connect a prediction to a robot simulation. Open-ended use without a purpose makes evaluation and safety difficult.",
                        "The goal is not early adoption for its own sake. It is literacy: students should be less easily impressed, more able to ask what a system can and cannot support, and more careful about their own responsibility."
                    ],
                ),
            ],
            [("AI program", "/programs/ai"), ("AI Guessing Game", "/projects/ai-guessing-game"), ("For Parents", "/parents")],
        ),
        "ai-is-not-magic-teaching-kids-to-question-it": article(
            "AI Is Not Magic: Teaching Kids to Question It",
            "AI for Kids",
            "The strongest AI lesson is not how to get an impressive answer. It is how to investigate where the answer came from and when it fails.",
            (
                "AI demonstrations often hide the difficult parts. A tool produces text, an image, or a prediction, and the result appears instantly. "
                "Children may reasonably conclude that the system knows. Education should reopen the box enough to replace magic language with testable ideas."
            ),
            [
                (
                    "Use precise verbs",
                    [
                        "A model predicts, classifies, generates, ranks, or matches patterns. Those verbs describe observable operations better than thinks, understands, or wants. Human-like language can be convenient, but it should not become the explanation.",
                        "Precision does not make the technology less interesting. It gives students a way to ask what evidence would distinguish one explanation from another."
                    ],
                ),
                (
                    "Collect failures deliberately",
                    [
                        "If a class shows only successful outputs, students learn performance rather than evaluation. A better activity asks related questions, changes one prompt condition, records inconsistencies, and groups the errors.",
                        "The Confidently Wrong Machine idea is useful because confidence becomes a variable to question. Does a polished answer include a source? Can the claim be verified? What kind of mistake appears repeatedly?"
                    ],
                ),
                (
                    "Bias is a system question",
                    [
                        "Patterns depend on examples and choices. If some cases are missing or labels are weak, results can be uneven. Children do not need advanced statistics to understand that an unrepresentative collection can produce a poor rule.",
                        "The conversation should stay concrete: Which examples did we test? Which group of cases failed? What information was absent? Avoid turning bias into a vague warning detached from evidence."
                    ],
                ),
                (
                    "Keep a human decision boundary",
                    [
                        "A useful classroom protocol states what the tool may support and what a person must verify. Generated possibilities may help brainstorming; factual claims need checking. A robot prediction may suggest an action; safety limits remain human-defined.",
                        "AI literacy is not obedience to a tool and not automatic rejection. It is the ability to use a system for a narrow purpose, inspect its limits, protect information, and retain responsibility for the result."
                    ],
                ),
            ],
            [("AI & Smart Machines", "/programs/ai"), ("Chatbot Character Lab", "/projects/chatbot-character-lab"), ("Debugging", "/topics/debugging")],
        ),
        "from-scratch-to-robots-to-ai": article(
            "From Scratch to Robots to AI",
            "Computer Lab Notes",
            "The pathway is not a race through tools. It is a growing web of events, state, sensing, feedback, and judgment.",
            (
                "Scratch, robotics, Roblox, and AI can look like separate subjects. A coherent curriculum treats them as different materials for recurring ideas. "
                "Events start behaviour. Variables preserve information. Conditions turn information into choices. Feedback connects action with evidence."
            ),
            [
                (
                    "Scratch makes the structure visible",
                    [
                        "A Scratch game gives beginners direct access to complete systems. The student can see event blocks, loops, conditions, variables, and messages. A coordinate change creates motion immediately; a state bug creates a visible contradiction.",
                        "This stage develops authorship. Students make a playable object, change rules, and explain the program as a text with sequence and intention."
                    ],
                ),
                (
                    "Robotics adds the physical world",
                    [
                        "The same program structures meet inputs, outputs, sensors, timing, circuits, and imperfect movement. A robot route depends on commands and direction. A patrol adds repeated sensing, decisions, state, and feedback.",
                        "Physical systems also make limitations unavoidable. Sensors vary, connections fail, and the environment changes. Students learn to separate code, hardware, and measurement questions."
                    ],
                ),
                (
                    "Text code expands expression",
                    [
                        "Roblox Studio / Lua can later connect visual programming concepts to functions, objects, 3D coordinates, and larger game systems. The blocks disappear, but events and variables do not.",
                        "The transition should happen because text code supports a new kind of project, not because visual programming has become embarrassing. A strong Scratch foundation makes the new syntax meaningful."
                    ],
                ),
                (
                    "AI adds uncertainty and judgment",
                    [
                        "AI systems return patterns, predictions, images, or language that may be useful and may be wrong. Earlier habits become essential: inspect inputs, reveal state where possible, test new cases, classify failures, and describe limits.",
                        "The sequence is an educational direction, not a mandatory ladder. Students may enter at different points and revisit ideas. Scratch and Robotics are active first; Roblox and AI are available later."
                    ],
                ),
            ],
            [("Programs", "/programs"), ("Topic library", "/topics"), ("Computer Lab", "/computer-lab")],
        ),
        "the-future-computer-lab-games-robots-and-smart-machines": article(
            "The Future Computer Lab: Games, Robots, and Smart Machines",
            "Computer Lab Notes",
            "A useful Computer Lab is not a room full of devices. It is structured time for ideas to be rebuilt across different materials.",
            (
                "The phrase computer lab can suggest either an old row of identical desktops or an unstructured room where children use whatever software they like. "
                "School of Code uses the term differently. The school provides the planned learning path. The Computer Lab provides guided project time in which a learned idea can change form."
            ),
            [
                (
                    "The class gives the idea",
                    [
                        "A coordinate lesson introduces x and y, known starting positions, prediction, and boundaries. The guided project develops those ideas inside Escape from the Giant Pigeon. Students share a conceptual foundation and clear checkpoints.",
                        "The class matters because freedom without vocabulary can become trial and error without learning. Theory is the skeleton that keeps later experiments understandable."
                    ],
                ),
                (
                    "The Lab gives the idea a life",
                    [
                        "Grandma's Intergalactic Taxi turns coordinates into destinations and routes. Astro-Chicken Rescue gives coordinates to several moving objects and a radar-like comparison. The projects differ, but the student can recognize the same position model underneath.",
                        "Structured freedom means the student can choose an implementation, challenge card, theme, or improvement while an instructor protects scope and asks for evidence."
                    ],
                ),
                (
                    "Different materials, connected concepts",
                    [
                        "A condition can control quiz feedback, a traffic-light transition, or a robot obstacle response. A variable can hold game score, reaction time, or patrol state. A bug can appear in code, a circuit, or the relationship between them.",
                        "A future Lab may include games, microcontrollers, simulations, simple electronics, robots, and carefully bounded AI experiments. The value comes from the conceptual connections, not the quantity of equipment."
                    ],
                ),
                (
                    "What the Lab must not become",
                    [
                        "It is not random gaming, passive video watching, uncontrolled browsing, or an excuse to collect fashionable tools. Students arrive with a project system, challenge, test, repair, or demonstration target.",
                        "The human scale matters. Small groups let the instructor understand the actual project, preserve student authorship, and help when a strange idea becomes too large to finish. The future Lab should remain a workshop, not a showroom."
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


def add_section(slug, heading, *paragraphs):
    BLOG_POSTS[slug]["sections"].append((heading, list(paragraphs)))


add_section(
    "is-coding-class-just-more-screen-time",
    "A simple after-class check",
    "Ask the student to open the project and make one small change in front of you. Change the player speed, move a safe zone, or explain why the score begins at zero. Active work leaves a structure the student can revisit. If the project cannot be changed without starting over, that is useful information about how much was understood.",
    "Also ask what failed. A real build usually contains a wrong turn: x changed instead of y, a loop ran forever, or restart preserved an old value. A student who can describe the failure and the repair has done more than operate an app. The child has compared intention with evidence and revised a system. That is the educational distinction School of Code is trying to protect.",
)
add_section(
    "what-age-should-kids-start-programming",
    "The first task should be finishable",
    "A suitable first task has a visible result within reach. Four-direction movement, a two-state traffic light, or a paper robot route can be enough. The child should encounter one meaningful problem without carrying the full complexity of art, accounts, hardware, and a giant game at the same time. Completion creates a stable object to discuss and improve.",
    "Adults can watch how support is used. Does the student follow a checkpoint, ask a specific question, and try again after a mismatch? Can the student explain one command even if the whole project required help? Those observations are more useful than comparing the child with a universal age chart. A conversation about fit can then use actual working habits rather than a birthday alone.",
)
add_section(
    "why-scratch-is-a-great-first-programming-language",
    "What good Scratch teaching avoids",
    "Dragging blocks is not automatically programming education. A lesson can still become mechanical if every student copies an instructor's finished script without predicting, testing, or changing anything. The useful question is whether the child understands the relationship among the blocks and the visible behaviour. A short script explained well has more educational value than a large unexplained stack.",
    "Good teaching also avoids treating the library of sprites and sounds as the main achievement. Artwork can support authorship, but a project needs a system: a rule that starts, changes, checks, remembers, or communicates. Students should leave able to identify that system, demonstrate one edge case, and make a deliberate modification. Scratch makes those conversations easier; it does not replace them.",
)
add_section(
    "why-debugging-is-good-for-kids",
    "Keep a small debugging record",
    "A useful record can be four lines: expected result, observed result, test, and conclusion. For a robot route, the student might write that the robot should face east after two turns, observed north, traced each command, and found that one left turn had been used instead of right. The format slows down random repair without turning the project into paperwork.",
    "The conclusion can also be that the first guess was wrong. That is not wasted effort. It narrows the search and teaches that evidence has authority over confidence. Over time, students build a vocabulary for recurring failures: unknown start, wrong sign, repeated event, stale state, loose connection, noisy reading. Naming patterns makes future debugging faster while preserving the habit of checking the current case.",
)
add_section(
    "robotics-for-kids-where-to-start",
    "Choose a first project by its question",
    "A useful first robotics project asks one question clearly. Can the robot follow an exact route? Can a button control a buzzer? Can an LED sequence move through safe states? Can a timer distinguish waiting from reacting? Each project exposes a different relationship among input, decision, and output. Buying a kit before choosing the question often leaves the learning goal buried under assembly.",
    "The project should also have a non-hardware fallback when the central idea permits it. A maze can be traced on paper; traffic-light state can be simulated on screen; a sensor rule can begin with recorded sample values. This is not pretending that hardware does not matter. It lets students understand the logic first, so a loose wire or drifting motor later becomes a specific system problem rather than undifferentiated failure.",
)
add_section(
    "how-robots-sense-the-world",
    "Run a classroom sensor investigation",
    "Before programming a response, students can make a small table of readings. Move an object to three distances, press and release a button several times, or compare light values in two parts of a room. Record what stayed stable, what varied, and which values overlap. The table turns a mysterious number into evidence about a limited measuring device.",
    "Only then choose a rule. If an alarm should sound when something is near, students can propose a threshold and test cases just above and below it. A good demonstration includes a case that fails or wobbles. The student can explain whether the limitation belongs to the sensor, the environment, the sampling method, or the decision rule. That explanation is more important than making the machine appear perfectly certain.",
)
add_section(
    "what-is-a-microcontroller",
    "What a microcontroller can and cannot do",
    "A microcontroller is good at repeating a defined cycle: read an input, update a value, choose an output, and do it again. It can time a reaction, control a traffic-light sequence, read a button, or signal when a threshold is crossed. Its small scale makes the relationship between code and physical pins easier to inspect than in a general-purpose computer.",
    "It does not understand why a reaction time is unusual or whether an alarm rule is fair. It follows the program with the available readings. Students therefore need to separate the board, the program, the circuit, and the human goal. When an LED stays dark, they can check output state, pin choice, polarity, connection, and component condition in an order. That layered diagnosis is part of the educational value.",
)
add_section(
    "why-robot-projects-teach-real-problem-solving",
    "Failure crosses system boundaries",
    "In a screen-only project, the visible result usually comes from code and stored state. A robot or circuit adds power, connections, components, measurement, timing, physical dimensions, and the environment. The same symptom can have several causes. A patrol that misses an obstacle may read the wrong sensor, use a poor threshold, move too quickly, or point the sensor in the wrong direction.",
    "Students learn to divide the system before repairing it. Can the sensor value be displayed without movement? Can the motor output be tested without the sensor rule? Does the simulated decision work with known sample values? Each test isolates a relationship. This is real problem-solving because the student cannot rely on one category of answer; the evidence determines whether to inspect logic, hardware, measurement, or assumptions about the world.",
)
add_section(
    "what-kids-learn-from-making-games",
    "Rules create an audience relationship",
    "A game communicates with a player through controls, goals, feedback, and consequences. If a hazard cannot be seen before contact, the rule may be technically correct and still feel unfair. If score changes twice for one event, the player receives false information. Students learn that code does not exist separately from the person trying to understand the system.",
    "Testing with another student can reveal assumptions the author no longer notices. The tester may use two keys at once, approach the goal from the wrong side, or restart during a message. The author then decides whether the behaviour is a bug, an acceptable rule, or a new design opportunity. That process joins programming with communication: the student must make the intended experience legible through the system itself.",
)
add_section(
    "roblox-as-a-creative-coding-platform",
    "Why waiting can be responsible",
    "A Roblox program needs more than student interest. The school must decide how accounts, privacy, publishing, external models, collaboration, and device performance will be handled. The instructor also needs a sequence that teaches Lua and game systems instead of letting Studio become a decoration tool or a collection of copied scripts. Marking the program Available Later keeps those requirements visible.",
    "In the meantime, Scratch and robotics can establish events, variables, conditions, functions, coordinates, state, and debugging. Those ideas transfer. A future Roblox student who already asks where state lives, what triggers an event, and whether an imported asset contains unknown behaviour will enter Studio with stronger habits. Delay is useful when it protects the educational purpose rather than chasing platform familiarity.",
)
add_section(
    "what-is-project-based-learning",
    "Completion is not decoration",
    "A project is not complete because the title screen looks polished. It needs a working core, a known start, a way to test success and failure, and an explanation of at least one design decision. For a traffic light, that means a safe state sequence and reset. For a game, it may mean movement, one goal, one hazard, and reliable restart before extra art or sound.",
    "This definition protects students from projects that grow faster than understanding. The instructor can reduce scope without removing authorship: keep one level, choose one sensor, or postpone the second character. Once a small version is demonstrable, improvements have evidence behind them. Students can compare versions and say what changed. Project-based learning works when the project carries the ideas, not when construction merely fills the timetable.",
)
add_section(
    "why-small-groups-work-better-for-coding",
    "What the instructor is watching",
    "The important signals are often quiet. A student may repeatedly press run without reading the result, avoid testing a loss state, change three scripts at once, or understand the concept but struggle to name it. In a small group, the instructor can notice the pattern and ask one relevant question instead of delivering the same rescue to everyone.",
    "Small groups also make demonstrations possible. Students can show a checkpoint, compare two solutions, and help a peer after first trying independently. The instructor can distinguish useful collaboration from one student taking over another's keyboard. This does not guarantee a fixed published group size; that operating detail is still being finalized. It explains why the school is designed around a human-sized group rather than maximum seat count.",
)
add_section(
    "can-kids-learn-ai-safely",
    "Design a bounded AI activity",
    "A safe first investigation has a narrow question, non-personal input, a defined tool, and a way to record errors. Students might compare how a guessing system handles new examples or test whether a fictional chatbot follows three written character rules. The task should not require private stories, personal photos, school records, or open-ended disclosure to an external service.",
    "Before use, the group needs to know what is being sent, whether an account is involved, what outputs may be unreliable, and who checks the result. Afterward, students should be able to show incorrect cases, not only impressive ones. School of Code marks AI Available Later because tool selection, privacy arrangements, and classroom boundaries must be settled before such an activity becomes an active offer.",
)
add_section(
    "ai-is-not-magic-teaching-kids-to-question-it",
    "Use an evidence table",
    "Students can record a prompt or input, the output, what was checked, the result of the check, and a failure category. Categories might include invented fact, missing context, inconsistent rule, biased example, or answer that cannot be verified. A table gives the class something firmer than saying an output felt good or sounded intelligent.",
    "The table also reveals that errors are not all repaired by a longer prompt. Sometimes the question lacks enough information. Sometimes the tool is inappropriate. Sometimes the source must be checked elsewhere, and sometimes a person should make the decision without the model. Treating these outcomes as normal teaches a more accurate picture: AI can produce useful patterns and fluent material, but responsibility does not transfer to the machine when the output appears polished.",
)
add_section(
    "from-scratch-to-robots-to-ai",
    "The path is a web, not a ladder",
    "Students do not need to complete every Scratch topic before touching a circuit, and robotics does not automatically graduate into AI. The direction describes recurring ideas, not ranks. A button-and-buzzer alarm may clarify events for a student who first met them in a game. A coordinate game may make a later robot map easier to discuss. Movement between programs can strengthen the shared concepts.",
    "Teachers should make those returns explicit. Ask where state lives in the pet game and the traffic light. Compare a Scratch touching check with a physical sensor threshold. Contrast a rule-based patrol with a future prediction system. The tools differ, but students can reuse habits: define input, name state, predict output, test edge cases, and explain limits.",
    "This is also why future programs should not be rushed. Text code and AI deserve a place when they support a project and when the student has enough conceptual language to question them. Scratch and Robotics are active first because they provide visible, testable systems now. Roblox and AI remain later branches, not badges that every child must collect.",
)
add_section(
    "the-future-computer-lab-games-robots-and-smart-machines",
    "Design the room around work, not equipment",
    "A useful Lab needs places to plan, build, test, explain, and safely store work. Some tasks belong on a screen; others need a paper grid, a circuit surface, spare components, or enough floor to trace movement. The room should make it easy to shift between code and evidence instead of keeping every student fixed in front of one device.",
    "The project system matters more than a catalogue of tools. Each activity needs a mission, required systems, checkpoints, challenge cards, and a demonstration target. Equipment enters when it gives an idea a useful physical form. A microcontroller can make timing tangible; a sensor can expose measurement; a robot can reveal feedback limits. None of them should exist only to make the Lab look advanced.",
    "Human organization completes the design. Small groups, clear component handling, privacy rules, and time to reset the workspace keep experimentation responsible. The School sets the conceptual path and the Lab offers structured freedom inside it. That relationship should remain true even as the range of machines grows.",
)


def extend_last_section(slug, paragraph):
    BLOG_POSTS[slug]["sections"][-1][1].append(paragraph)


extend_last_section(
    "why-scratch-is-a-great-first-programming-language",
    "A useful final question is whether the student could rebuild the core with a different theme. If pigeon, taxi, and chicken artwork can change while events, movement, state, and tests remain recognizable, the child is beginning to separate a program's structure from its surface. That separation supports later languages.",
)
extend_last_section(
    "why-debugging-is-good-for-kids",
    "Families can reinforce the method without demanding a technical explanation. Ask what was supposed to happen, what actually happened, and which single test produced useful evidence. Those questions reward reasoning instead of speed and make it normal for a finished demonstration to include the story of one repaired failure.",
)
extend_last_section(
    "robotics-for-kids-where-to-start",
    "A strong first sequence ends with explanation: the student names the input, the decision rule, the output, and one limit. That demonstration works whether the system used paper arrows, a simulation, LEDs, or a physical robot. The materials can grow after the model is understood.",
)
extend_last_section(
    "how-robots-sense-the-world",
    "The same method prepares students for later computer vision and AI discussions without claiming those systems are already being taught. More advanced sensing still begins with measurements, selected features, thresholds or models, uncertainty, and human decisions about what counts as success.",
)
extend_last_section(
    "what-is-a-microcontroller",
    "This is why the board should not be presented as a tiny magical brain. It is a constrained computer connected to physical inputs and outputs. Its constraints are useful: memory, timing, pins, and power force the project to state clearly what information matters and what action is actually possible.",
)
extend_last_section(
    "why-robot-projects-teach-real-problem-solving",
    "A demonstration should include the boundary between layers. The student might show that the decision works with known values but the sensor varies near the threshold, or that the circuit works while the timing rule is wrong. Locating the boundary is often the most sophisticated part of the project.",
)
extend_last_section(
    "what-kids-learn-from-making-games",
    "Authorship becomes visible in those revisions. Choosing a fairer warning, clearer restart, or more interesting risk is not decoration; it changes the rules another person experiences. Students learn that technical choices communicate values such as clarity, challenge, patience, and respect for the player.",
)
extend_last_section(
    "roblox-as-a-creative-coding-platform",
    "When the program does open, project pages should remain honest about what students create themselves, what built-in tools provide, and what comes from external assets. Understanding provenance and hidden scripts is part of programming responsibility, especially inside a platform built for sharing.",
)
extend_last_section(
    "what-is-project-based-learning",
    "The final explanation prevents a polished object from hiding shallow participation. Students should identify the concept, demonstrate the core, describe a decision, and name one unresolved limit. That conversation tells the instructor and family more than a screenshot of the finished stage.",
)
extend_last_section(
    "why-small-groups-work-better-for-coding",
    "The aim is not constant adult attention. It is timely attention that helps students return to independent work. A well-placed checkpoint can prevent twenty minutes of random changes; a patient pause can let the student discover that the variable never reset. Both decisions require seeing the learner and the system together.",
)
extend_last_section(
    "can-kids-learn-ai-safely",
    "Families should be told which activity is planned before a tool is used, not asked to infer it from the word AI. A guessing experiment, image classifier, and chatbot test have different inputs, risks, and learning goals. Clear naming makes meaningful consent and useful questioning possible.",
)
extend_last_section(
    "ai-is-not-magic-teaching-kids-to-question-it",
    "The student should leave able to say both what the system did usefully and where it failed. Praise without evidence becomes hype; rejection without investigation becomes fear. A tested, limited claim is the more demanding and more practical position.",
)
extend_last_section(
    "from-scratch-to-robots-to-ai",
    "A student's route can therefore bend. Someone drawn to circuits may meet variables through reaction time; a game designer may discover feedback through enemy movement. The program map provides direction while topic links preserve those alternate entrances. Knowledge grows by returning with a new material and a sharper question.",
)
extend_last_section(
    "the-future-computer-lab-games-robots-and-smart-machines",
    "Growth should be measured by the quality of projects and explanations, not the number of devices on shelves. If students can finish versions, test edge cases, connect ideas across materials, and demonstrate what changed, the Lab is doing its job. New equipment should earn its place by making one of those actions stronger.",
)


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
