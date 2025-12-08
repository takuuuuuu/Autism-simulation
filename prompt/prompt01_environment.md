## environment generation

def generate_classroom():
    # must-have items
    classroom = [
        "Red, green, and blue child-sized tables and chairs arranged in small groups",
        "A teacher's corner with a small desk and storage cabinet",
        "Unlocked personal-item cubbies labeled with each child's name",
        "Dinosaur stickers decorating walls, shelves, or learning corners",
        "A sensory-play corner with tactile materials",
        "A sink designed for young children washing hands and brushing teeth",
        "A utensil cabinet"
    ]

    # optional items
    optional_items = [
        "A picture book corner with cushions and a small bookshelf",
        "A pretend-play area with toy kitchen sets and dress-up costumes",
        "A block-building area with wooden blocks and construction toys",
        "A nature corner with plants, stones, leaves, magnifying glasses, and pet tank (small fish and snails)",
        "An art station with crayons, paint, paper, and easels",
        "A music corner with a piano, tambourines, xylophones, and small drums",
        "A science observation table with simple tools and specimens",
        "A soft carpet area for circle time",
        "A set of number cards used for math games",
        "Soft seating like bean bags or small sofas",
        "A weather and calendar board for morning meetings",
    ]

    # randomly select some optional items
    classroom += random.sample(optional_items, random.randint(3, 5))
    return classroom



def generate_corridor():
    # must-have items
    corridor = [
        "Wide hallway allowing free interaction for children",
        "Separate restrooms for boys and girls",
        "Clear signage for classroom numbers and directions",
        "Staircase leading from the classroom corridor to the outdoor activity area; Slippery."
    ]
    # optional items
    optional_items = [
        "Soft mats near classroom doors for shoe removal or resting",
        "Potted plants along the corridor",
        "Visual cues on the floor to guide walking paths or queuing"
    ]

    # randomly select some optional items
    corridor += random.sample(optional_items, random.randint(0, 2))
    return corridor


def generate_nap_room():
    # must-have items
    nap_room = [
        "Small beds or mats for each child, arranged neatly",
        "Soft pillows and light blankets for comfort",
        "Window coverings to block sunlight",
    ]

    # optional items
    optional_items = [
        "Stuffed animals or small comfort toys for children",
        "Visual routine chart for nap time",
        "Air purifier or gentle ventilation",
        "Floor rugs around beds for safe movement"
    ]

    # randomly select some optional items
    nap_room += random.sample(optional_items, random.randint(0, 2))
    return nap_room


def generate_playground():
    # must-have items
    playground = [
        "Sandpit with buckets, shovels, molds, and small construction toys for building castles or digging",
        "Water play area with small tables, cups, scoops, and floating toys for sensory play",
        "Treehouse structure for climbing, imaginative play, and lookout activities",
        "Climbing area including jungle gyms, rope ladders, slides, and soft mats underneath",
        "Large grassy lawn for running, tag, relay races, and group circle games",
        "Child-height outdoor handwashing station with soap, paper towels, and step stools for shorter children",
        "Shaded seating area with benches and chairs for rest, snacks, or teacher supervision"
    ]

    # optional items
    optional_items = [
        "Balance beams and stepping stones arranged as mini obstacle courses",
        "Small garden patch for planting flowers, vegetables, or observing insects",
        "Outdoor chalkboard or easels for drawing, painting, and collaborative art projects",
        "Portable balls, hoops, beanbags, and cones for sports and team games",
        "Nature corner with logs, rocks, tree stumps, and potted plants for observation and imaginative play",
        "Storage shed for outdoor toys, sports equipment, and seasonal materials",
        "Marked pathways for tricycle riding, running lanes, and obstacle challenges",
        "Interactive outdoor panels or musical instruments like xylophones and drums"
    ]

    # randomly select some optional items
    playground += random.sample(optional_items, random.randint(2, 4))
    return playground


def generate_gate_area():
    # must-have items
    gate_area = [
        "Fenced entrance with secure gate, where children are dropped off and picked up",
        "Morning Health Check area with thermometer, hand sanitizer, and visual checklist",
    ]
    return gate_area


def generate_preschool():
    preschool = {
        "classroom": generate_classroom(),
        "corridor": generate_corridor(),
        "nap_room": generate_nap_room(),
        "playground": generate_playground(),
        "gate_area": generate_gate_area()
    }
    return preschool



## shared_memory and daily_schedule

shared_memories = [
    "This is a large preschool known for its child-centered, inclusive, and nature-based educational philosophy.",

    "The kindergarten adheres to principles that respect children's natural tendencies, individual differences, and diverse developmental needs. Teachers encourage autonomy, emotional expression, peer cooperation, and exploration of both natural and social environments.",

    "The school operates across multiple connected areas. Children in the middle class (ages 4–5) spend most of their time on the second floor, which includes the classroom, nap room, and corridor. The corridor leads down to the first-floor outdoor area, where the gate_area and playground are located. Children of this age are still very young and often engage in playful or mischievous behaviors. Their homeroom teacher is Miss T.",
    
    "The teaching team is highly professional and experienced. They frequently encourage children to talk about their feelings, conflicts, cooperation, and discoveries.",
    
    "Today is September 1st, 2025, the first day of school. Many children are new to the campus and extremely curious. Almost everyone wants to explore the environment and make new friends.",
    
    "It is now 7:30 a.m. Children are gradually arriving at the gate_area to begin their first day. The campus is filled with energy and excitement."



    daily_schedule = [
        {
            "time": "07:30 – 08:00",
            "activity": "Arrival · Morning Health Check · Morning Exercise",
            "details": [
                "Children arrive one after another. The teacher MissT greets them and conducts basic health checks, including checking nails, teeth, and overall cleanliness",
                "If a child’s nails are long or teeth unbrushed, MissT helps them trim nails or brush teeth.",
                "After the check, children join a simple morning exercise routine in a designated outdoor area led by MissT.",
                "Interactions include greetings, separation from parents, emotional soothing, and children observing and joining peers.",
                "Environment: gate area"
            ]
        },
        {
            "time": "8:00 – 08:20",
            "activity": "Breakfast",
            "details": [
                "Breakfast is served afterwards. MissT helps children wash their hands, guides them to sit properly, and encourage polite table manners.",
                "Interactions include greetings, separation from parents, emotional soothing, and children observing and joining peers.",
                "Environment: classroom."
            ]
        },
        {
            "time": "08:20 – 09:30",
            "activity": "Ice-breaking · Warm-up Activities · Getting to Know Teachers & Peers",
            "details": [
                "MissT introduce herself, classroom routines, and basic rules in a playful and friendly manner.",
                "Children participate in name games, circle games, role-play introductions, or simple cooperative tasks.",
                "MissT pay special attention to newly enrolled children, supporting shy or anxious children and facilitating peer bonding.",
                "The focus is on building group belonging, helping children remember each other’s names, and establishing trust in teachers.",
                "Environment: classroom"
            ]
        },
        {
            "time": "09:30 – 11:20",
            "activity": "Outdoor Autonomous Play · Game Review · Topic Discussion",
            "details": [
                "Children enter the outdoor activity area (sandpit, climbing frames, lawn, balance beams, tricycles). They choose activities freely.",
                "MissT observe children’s exploration, mediate conflicts, ensure safety, and document interesting behaviors.",
                "After play, MissT hold a short reflection circle: children share what they played, how they felt, and how they solved problems.",
                "If conflicts happened, the teacher guides the group to discuss what happened, how to express needs, and how to repair relationships.",
                "Positive behaviors—like taking turns, helping peers, or creative ideas—are publicly acknowledged.",
                "Environment: playground"
            ]
        },
        {
            "time": "11:30 – 11:50",
            "activity": "Lunch · Teeth Brushing",
            "details": [
                "Children wash hands, line up, and enter the dining area. MissT guide them to use utensils properly and try different foods.",
                "MissT then assist children in brushing teeth.",
                "Environment: classroom"
            ]
        },
        {
            "time": "11:50 – 12:15",
            "activity": "Post-meal Walk",
            "details": [
                "After lunch, children take a short walk in the hallway or outdoor zone to aid digestion.",
                "Free interactions in corridor",
                "Environment: corridor"
            ]
        },
        {
            "time": "12:15 – 14:15",
            "activity": "Nap Time",
            "details": [
                "Children settle into small beds in the nap room. MissT help them change into comfortable clothing, dim lights, and maintain a quiet atmosphere.",
                "Some younger or new children may need patting or verbal comfort to fall asleep.",
                "MissT stay in the room for supervision, ensuring safety and emotional comfort.",
                "Environment: nap room"
            ]
        },
        {
            "time": "14:15 – 14:45",
            "activity": "Wake-up · Afternoon Snack & Water",
            "details": [
                "MissT gently wake children, assist with dressing, and guide them to the snack area.",
                "Snacks may include fruits, small pastries, or yogurt. Children are reminded to drink water.",
                "MissT check if anyone still feels sleepy or uncomfortable and offer comfort.",
                "Environment: nap room"
            ]
        },

        {
            "time": "14:45 – 15:15",
            "activity": "Small-group Activities · Free Play",
            "details": [
                "Children form interest-based groups—block building, drawing, storybooks, music, pretend play, or simple science experiments.",
                "MissT support groups by offering materials, asking guiding questions, and documenting children's collaborative behaviors.",
                "This session emphasizes autonomy, creativity, and cooperative problem-solving.",
                "Environment: classroom
            ]
        },
        {
            "time": "15:15 – 16:15",
            "activity": "Outdoor Autonomous Play · Game Review · Topic Discussion",
            "details": [
                "A second outdoor play session. Children often choose similar games from the morning but may expand or combine activities.",
                "MissT observe developmental changes throughout the day (e.g., growing confidence, new friendships).",
                "Reflection and discussion follow the play, with emphasis on emotional sharing, cooperation, and emerging interests.",
                "Environment: playground"
            ]
        },

        {
            "time": "16:15 – 16:45",
            "activity": "Dinner Preparation · Dinner · Clean-up",
            "details": [
                "Children wash hands and prepare for dinner. MissT encourage independence such as carrying their own plates.",
                "Dinner is calmer than lunch; children are usually more relaxed after a full day.",
                "After eating, children help clean up—throwing away food scraps, wiping tables with guidance, and tidying belongings."
                "Environment: classroom
            ]
        },

        {
            "time": "16:55 – 17:30",
            "activity": "Dismissal & Parent Pick-up",
            "details": [
                "MissT lead children to the designated pick-up area. One MissT verifies each child’s guardian before dismissal.",
                "During waiting time, children talk quietly with peers.",
                "MissT share quick updates with parents if needed (e.g., meals, mood, friendships, small conflicts).",
                "Children say goodbye to MissT and classmates—a key social ritual."
                "Environment: gate area"
            ]
        }
    ]


    ]


    