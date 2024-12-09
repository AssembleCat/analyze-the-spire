def add_upgraded_cards(card_list):
    upgraded_list = []
    for card in card_list:
        upgraded_list.append(card)
        upgraded_list.append(card + "+1")
    return upgraded_list


# 직업별 [IRONCLAD, SILENT, DEFECT, WATCHER, COLORLESS]
# 희귀도별 [BASIC, COMMON, UNCOMMON, RARE, SPECIAL]
# 타입별 [ATTACK, SKILL, POWER]
# 상태이상/저주카드 [STATUS, CURSE]

# IRONCLAD
# 일반 공격 14장 + 타격 + 강타
IRONCLAD_ATTACK_COMMON = ['Anger', 'Bash', 'Body Slam', 'Clash', 'Cleave', 'Clothesline', 'Headbutt', 'Heavy Blade', 'Iron Wave', 'Perfected Strike',
                          'Pommel Strike', 'Strike_R', 'Sword Boomerang', 'Thunderclap', 'Twin Strike', 'Wild Strike']
# 특별 공격 11장
IRONCLAD_ATTACK_UNCOMMON = ['Blood for Blood', 'Carnage', 'Dropkick', 'Hemokinesis', 'Pummel', 'Rampage', 'Reckless Charge', 'Searing Blow',
                            'Sever Soul', 'Uppercut', 'Whirlwind']
# 희귀 공격 5장
IRONCLAD_ATTACK_RARE = ['Bludgeon', 'Feed', 'Fiend Fire', 'Immolate', 'Reaper']
# 일반 스킬 6장 + 수비
IRONCLAD_SKILL_COMMON = ['Armaments', 'Defend_R', 'Flex', 'Havoc', 'Shrug It Off', 'True Grit', 'Warcry']
# 특별 스킬 17장
IRONCLAD_SKILL_UNCOMMON = ['Battle Trance', 'Bloodletting', 'Burning Pact', 'Disarm', 'Dual Wield', 'Entrench', 'Flame Barrier', 'Ghostly Armor',
                           'Infernal Blade', 'Intimidate', 'Power Through', 'Rage', 'Second Wind', 'Seeing Red', 'Sentinel', 'Shockwave',
                           'Spot Weakness']
# 희귀 스킬 5장
IRONCLAD_SKILL_RARE = ['Double Tap', 'Exhume', 'Impervious', 'Limit Break', 'Offering']
# 특별 파워 8장
IRONCLAD_POWER_UNCOMMON = ['Combust', 'Dark Embrace', 'Evolve', 'Feel No Pain', 'Fire Breathing', 'Inflame', 'Metallicize', 'Rupture']
# 희귀 파워 6장
IRONCLAD_POWER_RARE = ['Barricade', 'Berserk', 'Brutality', 'Corruption', 'Demon Form', 'Juggernaut']

# SILENT
# 일반 공격 9장 + 타격 + 약화
SILENT_ATTACK_COMMON = ['Bane', 'Dagger Spray', 'Dagger Throw', 'Flying Knee', 'Neutralize', 'Poisoned Stab', 'Quick Slash', 'Slice',
                        'Strike_G', 'Sucker Punch', 'Underhanded Strike']
# 특별 공격 13장
SILENT_ATTACK_UNCOMMON = ['All Out Attack', 'Backstab', 'Choke', 'Dash', 'Endless Agony', 'Eviscerate', 'Finisher', 'Flechettes', 'Heel Hook',
                          'Masterful Stab', 'Predator', 'Riddle With Holes', 'Skewer']
# 희귀 공격 4장
SILENT_ATTACK_RARE = ['Die Die Die', 'Glass Knife', 'Grand Finale', 'Unload']
# 일반 스킬 10장 + 수비 + 생존자
SILENT_SKILL_COMMON = ['Acrobatics', 'Backflip', 'Blade Dance', 'Cloak And Dagger', 'Deadly Poison', 'Deflect', 'Defend_G', 'Dodge and Roll',
                       'Outmaneuver', 'PiercingWail', 'Prepared', 'Survivor']
# 특별 스킬 14장
SILENT_SKILL_UNCOMMON = ['Blur', 'Bouncing Flask', 'Calculated Gamble', 'Catalyst', 'Concentrate', 'Crippling Poison', 'Distraction', 'Escape Plan',
                         'Expertise', 'Leg Sweep', 'Reflex', 'Setup', 'Tactician', 'Terror']
# 희귀 스킬 10장 -> Venomology 연금, Night Terror 악몽
SILENT_SKILL_RARE = ['Adrenaline', 'Bullet Time', 'Burst', 'Corpse Explosion', 'Doppelganger', 'Malaise', 'Night Terror', 'Phantasmal Killer',
                     'Storm of Steel', 'Venomology']
# 특별 파워 6장
SILENT_POWER_UNCOMMON = ['Accuracy', 'Caltrops', 'Footwork', 'Infinite Blades', 'Noxious Fumes', 'Well Laid Plans']
# 희귀 파워 5장
SILENT_POWER_RARE = ['A Thousand Cuts', 'After Image', 'Envenom', 'Tools of the Trade', 'Wraith Form v2']

# DEFECT
# 일반 공격 10장 + 타격
DEFECT_ATTACK_COMMON = ['Ball Lightning', 'Barrage', 'Beam Cell', 'Cold Snap', 'Compile Driver', 'Gash', 'Go for the Eyes', 'Rebound', 'Strike_B',
                        'Streamline', 'Sweeping Beam']
# 특별 공격 8장
DEFECT_ATTACK_UNCOMMON = ['Blizzard', 'Doom and Gloom', 'FTL', 'Lockon', 'Rip and Tear', 'Melter', 'Scrape', 'Sunder']
# 희귀 공격 5장
DEFECT_ATTACK_RARE = ['All For One', 'Core Surge', 'Hyperbeam', 'Meteor Strike', 'Thunder Strike']
# 일반 스킬 8장 + 수비 + 이중시전 + 파지직 -> Steam 증기방벽
DEFECT_SKILL_COMMON = ['Conserve Battery', 'Coolheaded', 'Defend_B', 'Dualcast', 'Hologram', 'Leap', 'Redo', 'Stack', 'Steam', 'Turbo', 'Zap']
# 특별 스킬 20장 -> Steam Power 오버클럭, Undo 평형
DEFECT_SKILL_UNCOMMON = ['Aggregate', 'Auto Shields', 'BootSequence', 'Chaos', 'Chill', 'Consume', 'Darkness', 'Double Energy', 'Force Field',
                         'Fusion', 'Genetic Algorithm', 'Glacier', 'Recycle', 'Reinforced Body', 'Reprogram', 'Skim', 'Steam Power', 'Tempest',
                         'Undo', 'White Noise']
# 희귀 스킬 6장
DEFECT_SKILL_RARE = ['Amplify', 'Fission', 'Multi-Cast', 'Rainbow', 'Reboot', 'Seek']
# 특별 파워 8장
DEFECT_POWER_UNCOMMON = ['Capacitor', 'Defragment', 'Heatsinks', 'Hello World', 'Loop', 'Self Repair', 'Static Discharge', 'Storm']
# 희귀 파워 6장
DEFECT_POWER_RARE = ['Biased Cognition', 'Buffer', 'Creative AI', 'Echo Form', 'Electrodynamics', 'Machine Learning']

# WATCHER
# 일반 공격 10장 + 티격 + 진노
WATCHER_ATTACK_COMMON = ['BowlingBash', 'Consecrate', 'CrushJoints', 'CutThroughFate', 'EmptyFist', 'Eruption', 'FlurryOfBlows', 'FlyingSleeves',
                         'FollowUp', 'JustLucky', 'SashWhip', 'Strike_P']
# 특별 공격 12장
WATCHER_ATTACK_UNCOMMON = ['CarveReality', 'Conclude', 'FearNoEvil', 'ReachHeaven', 'SandsOfTime', 'SignatureMove', 'TalkToTheHand', 'Tantrum',
                           'Wallop', 'Weave', 'WheelKick', 'WindmillStrike']
# 희귀 공격 3장
WATCHER_ATTACK_RARE = ['Brilliance', 'LessonLearned', 'Ragnarok']
# 일반 스킬 9장 + 수비 + 경각
WATCHER_SKILL_COMMON = ['ClearTheMind', 'Crescendo', 'Defend_P', 'EmptyBody', 'Evaluate', 'Halt', 'PathToVictory', 'Prostrate', 'Protect', 'ThirdEye',
                        'Vigilance']
# 특별 스킬 15장
WATCHER_SKILL_UNCOMMON = ['Blasphemy', 'Collect', 'DeceiveReality', 'EmptyMind', 'ForeignInfluence', 'Indignation', 'InnerPeace', 'Meditate',
                          'Perseverance', 'Pray', 'Sanctity', 'Swivel', 'WaveOfTheHand', 'Worship', 'WreathOfFlame']
# 희귀 스킬 10장 -> Vengeance 신성모독
# Wish choice = [BecomeAlmighty, FameAndFortune, LiveForever]
WATCHER_SKILL_RARE = ['Alpha', 'ConjureBlade', 'DeusExMachina', 'Judgement', 'Omniscience', 'Scrawl', 'SpiritShield', 'Vault', 'Vengeance', 'Wish']
# 특별 파워 8장 -> Adaptation 추월, Wireheading 예지
WATCHER_POWER_UNCOMMON = ['Adaptation', 'BattleHymn', 'Fasting2', 'LikeWater', 'MentalFortress', 'Nirvana', 'Study', 'Wireheading']
# 희귀 파워 4장
WATCHER_POWER_RARE = ['DevaForm', 'Devotion', 'Establishment', 'MasterReality']

# COLORLESS
# 특별 공격 4장
COLORLESS_ATTACK_UNCOMMON = ['Dramatic Entrance', 'Flash of Steel', 'Mind Blast', 'Swift Strike']
# 희귀 공격 1장
COLORLESS_ATTACK_RARE = ['HandOfGreed']
# 스페셜 공격 6장
COLORLESS_ATTACK_SPECIAL = ['Bite', 'Expunger', 'RitualDagger', 'Shiv', 'Smite', 'ThroughViolence']
# 특별 스킬 16장
COLORLESS_SKILL_UNCOMMON = ['Bandage Up', 'Blind', 'Dark Shackles', 'Deep Breath', 'Discovery', 'Enlightenment', 'Finesse', 'Forethought',
                            'Good Instincts', 'Impatience', 'Jack Of All Trades', 'Madness', 'Panacea', 'PanicButton', 'Purity', 'Trip']
# 희귀 스킬 10장
COLORLESS_SKILL_RARE = ['Apotheosis', 'Chrysalis', 'Master of Strategy', 'Metamorphosis', 'Secret Technique', 'Secret Weapon', 'The Bomb',
                        'Thinking Ahead', 'Transmutation', 'Violence']
# 스페셜 스킬 6장 -> Ghostly 유체화
COLORLESS_SKILL_SPECIAL = ['Beta', 'Ghostly', 'Insight', 'J.A.X.', 'Miracle', 'Safety']
# 희귀 파워 4장
COLORLESS_POWER_RARE = ['Magnetism', 'Mayhem', 'Panache', 'Sadistic Nature']
# 스페셜 파워 1장
COLORLESS_POWER_SPECIAL = ['Omega']

# STATUS/CURSE
# 상태이상 5장
BASE_STATUS_CARD = ['Burn', 'Dazed', 'Slimed', 'Void', 'Wound']
# 저주 14장
BASE_CURSE_CARD = ['AscendersBane', 'Clumsy', 'CurseOfTheBell', 'Decay', 'Doubt', 'Injury', 'Necronomicurse', 'Normality', 'Pain', 'Parasite',
                   'Pride', 'Regret', 'Shame', 'Writhe']

# 카드 조합
IRONCLAD_ATTACK_CARD = IRONCLAD_ATTACK_COMMON + IRONCLAD_ATTACK_UNCOMMON + IRONCLAD_ATTACK_RARE
IRONCLAD_SKILL_CARD = IRONCLAD_SKILL_COMMON + IRONCLAD_SKILL_UNCOMMON + IRONCLAD_SKILL_RARE
IRONCLAD_POWER_CARD = IRONCLAD_POWER_UNCOMMON + IRONCLAD_POWER_RARE
IRONCLAD_COMMON_CARD = IRONCLAD_ATTACK_COMMON + IRONCLAD_SKILL_COMMON
IRONCLAD_UNCOMMON_CARD = IRONCLAD_ATTACK_UNCOMMON + IRONCLAD_SKILL_UNCOMMON + IRONCLAD_POWER_UNCOMMON
IRONCLAD_RARE_CARD = IRONCLAD_ATTACK_RARE + IRONCLAD_SKILL_RARE + IRONCLAD_POWER_RARE

SILENT_ATTACK_CARD = SILENT_ATTACK_COMMON + SILENT_ATTACK_UNCOMMON + SILENT_ATTACK_RARE
SILENT_SKILL_CARD = SILENT_SKILL_COMMON + SILENT_SKILL_UNCOMMON + SILENT_SKILL_RARE
SILENT_POWER_CARD = SILENT_POWER_UNCOMMON + SILENT_POWER_RARE
SILENT_COMMON_CARD = SILENT_ATTACK_COMMON + SILENT_SKILL_COMMON
SILENT_UNCOMMON_CARD = SILENT_ATTACK_UNCOMMON + SILENT_SKILL_UNCOMMON + SILENT_POWER_UNCOMMON
SILENT_RARE_CARD = SILENT_ATTACK_RARE + SILENT_SKILL_RARE + SILENT_POWER_RARE

DEFECT_ATTACK_CARD = DEFECT_ATTACK_COMMON + DEFECT_ATTACK_UNCOMMON + DEFECT_ATTACK_RARE
DEFECT_SKILL_CARD = DEFECT_SKILL_COMMON + DEFECT_SKILL_UNCOMMON + DEFECT_SKILL_RARE
DEFECT_POWER_CARD = DEFECT_POWER_UNCOMMON + DEFECT_POWER_RARE
DEFECT_COMMON_CARD = DEFECT_ATTACK_COMMON + DEFECT_SKILL_COMMON
DEFECT_UNCOMMON_CARD = DEFECT_ATTACK_UNCOMMON + DEFECT_SKILL_UNCOMMON + DEFECT_POWER_UNCOMMON
DEFECT_RARE_CARD = DEFECT_ATTACK_RARE + DEFECT_SKILL_RARE + DEFECT_POWER_RARE

WATCHER_ATTACK_CARD = WATCHER_ATTACK_COMMON + WATCHER_ATTACK_UNCOMMON + WATCHER_ATTACK_RARE
WATCHER_SKILL_CARD = WATCHER_SKILL_COMMON + WATCHER_SKILL_UNCOMMON + WATCHER_SKILL_RARE
WATCHER_POWER_CARD = WATCHER_POWER_UNCOMMON + WATCHER_POWER_RARE
WATCHER_COMMON_CARD = WATCHER_ATTACK_COMMON + WATCHER_SKILL_COMMON
WATCHER_UNCOMMON_CARD = WATCHER_ATTACK_UNCOMMON + WATCHER_SKILL_UNCOMMON + WATCHER_POWER_UNCOMMON
WATCHER_RARE_CARD = WATCHER_ATTACK_RARE + WATCHER_SKILL_RARE + WATCHER_POWER_RARE

COLORLESS_ATTACK_CARD = COLORLESS_ATTACK_UNCOMMON + COLORLESS_ATTACK_RARE + COLORLESS_ATTACK_SPECIAL
COLORLESS_SKILL_CARD = COLORLESS_SKILL_UNCOMMON + COLORLESS_SKILL_RARE + COLORLESS_SKILL_SPECIAL
COLORLESS_POWER_CARD = COLORLESS_POWER_RARE + COLORLESS_POWER_SPECIAL
COLORLESS_UNCOMMON_CARD = COLORLESS_ATTACK_UNCOMMON + COLORLESS_SKILL_UNCOMMON
COLORLESS_RARE_CARD = COLORLESS_ATTACK_RARE + COLORLESS_SKILL_RARE + COLORLESS_POWER_RARE
COLORLESS_SPECIAL_CARD = COLORLESS_ATTACK_SPECIAL + COLORLESS_SKILL_SPECIAL + COLORLESS_POWER_SPECIAL

BASE_ATTACK_CARD = IRONCLAD_ATTACK_CARD + SILENT_ATTACK_CARD + DEFECT_ATTACK_CARD + WATCHER_ATTACK_CARD + COLORLESS_ATTACK_CARD
BASE_SKILL_CARD = IRONCLAD_SKILL_CARD + SILENT_SKILL_CARD + DEFECT_SKILL_CARD + WATCHER_SKILL_CARD + COLORLESS_SKILL_CARD
BASE_POWER_CARD = IRONCLAD_POWER_CARD + SILENT_POWER_CARD + DEFECT_POWER_CARD + WATCHER_POWER_CARD + COLORLESS_POWER_CARD
BASE_COMMON_CARD = IRONCLAD_COMMON_CARD + SILENT_COMMON_CARD + DEFECT_COMMON_CARD + WATCHER_COMMON_CARD
BASE_UNCOMMON_CARD = IRONCLAD_UNCOMMON_CARD + SILENT_UNCOMMON_CARD + DEFECT_UNCOMMON_CARD + WATCHER_UNCOMMON_CARD + COLORLESS_UNCOMMON_CARD
BASE_RARE_CARD = IRONCLAD_RARE_CARD + SILENT_RARE_CARD + DEFECT_RARE_CARD + WATCHER_RARE_CARD + COLORLESS_RARE_CARD
BASE_SPECIAL_CARD = COLORLESS_SPECIAL_CARD

IRONCLAD_CARD = IRONCLAD_ATTACK_CARD + IRONCLAD_SKILL_CARD + IRONCLAD_POWER_CARD
SILENT_CARD = SILENT_ATTACK_CARD + SILENT_SKILL_CARD + SILENT_POWER_CARD
DEFECT_CARD = DEFECT_ATTACK_CARD + DEFECT_SKILL_CARD + DEFECT_POWER_CARD
WATCHER_CARD = WATCHER_ATTACK_CARD + WATCHER_SKILL_CARD + WATCHER_POWER_CARD
COLORLESS_CARD = COLORLESS_UNCOMMON_CARD + COLORLESS_RARE_CARD + COLORLESS_SPECIAL_CARD

# 덱에 존재할 수 있는 모든 카드
CAN_EXIST_IN_DECK = add_upgraded_cards(BASE_ATTACK_CARD + BASE_SKILL_CARD + BASE_POWER_CARD) + BASE_CURSE_CARD

# 모든카드
ALL_CARDS = CAN_EXIST_IN_DECK + BASE_STATUS_CARD

# 캐릭터 4종류
ALL_CHARACTERS = ['DEFECT', 'IRONCLAD', 'THE_SILENT', 'WATCHER']

# 유물 178종류 -> 삭제된 유물 제거버전 ('Circlet(관)', 'Dodecahedron(룬 12면체 2020/01/14 삭제 유물) <- 근데 정보가 있네? 일단 넣어', 'Discerning Monocle(2018/01/21 삭제 유물)')
ALL_RELICS = ['Akabeko', 'Anchor', 'Ancient Tea Set', 'Art of War', 'Astrolabe', 'Bag of Marbles', 'Bag of Preparation', 'Bird Faced Urn',
              'Black Blood', 'Black Star', 'Blood Vial', 'Bloody Idol', 'Blue Candle', 'Boot', 'Bottled Flame', 'Bottled Lightning',
              'Bottled Tornado', 'Brimstone', 'Bronze Scales', 'Burning Blood', 'Busted Crown', 'Cables', 'Calipers', 'Calling Bell', 'CaptainsWheel',
              'Cauldron', 'Centennial Puzzle', 'CeramicFish', 'Champion Belt', "Charon's Ashes", 'Chemical X', 'CloakClasp', 'ClockworkSouvenir',
              'Coffee Dripper', 'Cracked Core', 'CultistMask', 'Cursed Key', 'Damaru', 'Darkstone Periapt', 'DataDisk', 'Dead Branch', 'Dodecahedron',
              'DollysMirror', 'Dream Catcher', 'Du-Vu Doll', 'Ectoplasm', 'Emotion Chip', 'Empty Cage', 'Enchiridion', 'Eternal Feather',
              'FaceOfCleric', 'FossilizedHelix', 'Frozen Egg 2', 'Frozen Eye', 'FrozenCore', 'Fusion Hammer', 'Gambling Chip', 'Ginger', 'Girya',
              'Golden Idol', 'GoldenEye', 'Gremlin Horn', 'GremlinMask', 'HandDrill', 'Happy Flower', 'HolyWater', 'HornCleat', 'HoveringKite',
              'Ice Cream', 'Incense Burner', 'InkBottle', 'Inserter', 'Juzu Bracelet', 'Kunai', 'Lantern', "Lee's Waffle", 'Letter Opener',
              'Lizard Tail', 'Magic Flower', 'Mango', 'Mark of Pain', 'Mark of the Bloom', 'Matryoshka', 'MawBank', 'MealTicket', 'Meat on the Bone',
              'Medical Kit', 'Melange', 'Membership Card', 'Mercury Hourglass', 'Molten Egg 2', 'Mummified Hand', 'MutagenicStrength', 'Necronomicon',
              'NeowsBlessing', "Nilry's Codex", 'Ninja Scroll', "Nloth's Gift", 'NlothsMask', 'Nuclear Battery', 'Nunchaku', 'Odd Mushroom',
              'Oddly Smooth Stone', 'Old Coin', 'Omamori', 'OrangePellets', 'Orichalcum', 'Ornamental Fan', 'Orrery', "Pandora's Box", 'Pantograph',
              'Paper Crane', 'Paper Frog', 'Peace Pipe', 'Pear', 'Pen Nib', "Philosopher's Stone", 'Pocketwatch', 'Potion Belt', 'Prayer Wheel',
              'PreservedInsect', 'PrismaticShard', 'PureWater', 'Question Card', 'Red Mask', 'Red Skull', 'Regal Pillow', 'Ring of the Serpent',
              'Ring of the Snake', 'Runic Capacitor', 'Runic Cube', 'Runic Dome', 'Runic Pyramid', 'SacredBark', 'Self Forming Clay', 'Shovel',
              'Shuriken', 'Singing Bowl', 'SlaversCollar', 'Sling', 'Smiling Mask', 'Snake Skull', 'Snecko Eye', 'Sozu', 'Spirit Poop',
              'SsserpentHead', 'StoneCalendar', 'Strange Spoon', 'Strawberry', 'StrikeDummy', 'Sundial', 'Symbiotic Virus', 'TeardropLocket',
              'The Courier', 'The Specimen', 'TheAbacus', 'Thread and Needle', 'Tingsha', 'Tiny Chest', 'Tiny House', 'Toolbox', 'Torii',
              'Tough Bandages', 'Toxic Egg 2', 'Toy Ornithopter', 'TungstenRod', 'Turnip', 'TwistedFunnel', 'Unceasing Top', 'Vajra', 'Velvet Choker',
              'VioletLotus', 'War Paint', 'WarpedTongs', 'Whetstone', 'White Beast Statue', 'WingedGreaves', 'WristBlade', 'Yang']
# 모든 이벤트 72종류
ALL_ENEMY = ['2 Fungi Beasts', '2 Louse', '2 Orb Walkers', '2 Thieves', '3 Byrds', '3 Cultists', '3 Darklings', '3 Louse', '3 Sentries',
             '3 Shapes', '4 Byrds', '4 Shapes', 'Apologetic Slime', 'Automaton', 'Awakened One', 'Blue Slaver', 'Book of Stabbing',
             'Centurion and Healer', 'Champ', 'Chosen', 'Chosen and Byrds', 'Collector', 'Colosseum Nobs', 'Colosseum Slavers', 'Cultist',
             'Cultist and Chosen', 'Donu and Deca', 'Exordium Thugs', 'Exordium Wildlife', 'Flame Bruiser 1 Orb', 'Flame Bruiser 2 Orb',
             'Giant Head', 'Gremlin Gang', 'Gremlin Leader', 'Gremlin Nob', 'Hexaghost', 'Jaw Worm', 'Jaw Worm Horde', 'Lagavulin',
             'Lagavulin Event', 'Large Slime', 'Looter', 'Lots of Slimes', 'Masked Bandits', 'Maw', 'Mind Bloom Boss Battle',
             'Mysterious Sphere', 'Nemesis', 'Orb Walker', 'Red Slaver', 'Reptomancer', 'Sentry and Sphere', 'Shell Parasite',
             'Shelled Parasite and Fungi', 'Shield and Spear', 'Slaver and Parasite', 'Slavers', 'Slime Boss', 'Small Slimes', 'Snake Plant',
             'Snecko', 'Snecko and Mystics', 'Sphere and 2 Shapes', 'Spheric Guardian', 'Spire Growth', 'The Eyes',
             'The Guardian', 'The Heart', 'The Mushroom Lair', 'Time Eater', 'Transient', 'Writhing Mass']
