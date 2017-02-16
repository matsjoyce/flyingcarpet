import enum
import logging


logger = logging.getLogger(__name__)


class Category(enum.Enum):
    AudioVideo = "AudioVideo"    # Application for presenting, creating, or processing multimedia (audio/video)
    Audio = "Audio"              # An audio application
    Video = "Video"              # A video application
    Development = "Development"  # An application for development
    Education = "Education"      # Educational software
    Game = "Game"                # A game
    Graphics = "Graphics"        # Application for viewing, creating, or processing graphics
    Network = "Network"          # Network application such as a web browser
    Office = "Office"            # An office type application
    Science = "Science"          # Scientific software
    Settings = "Settings"        # Settings applications
    System = "System"            # System application, "System Tools" such as say a log viewer or network monitor
    Utility = "Utility"          # Small utility application, "Accessories"


class SubCategory(enum.Enum):
    # A tool to build applications
    Building = ("Building", {Category.Development})

    # A tool to debug applications
    Debugger = ("Debugger", {Category.Development})

    # IDE application
    IDE = ("IDE", {Category.Development})

    # A GUI designer application
    GUIDesigner = ("GUIDesigner", {Category.Development})

    # A profiling tool
    Profiling = ("Profiling", {Category.Development})

    # Applications like cvs or subversion
    RevisionControl = ("RevisionControl", {Category.Development})

    # A translation tool
    Translation = ("Translation", {Category.Development})

    # Calendar application
    Calendar = ("Calendar", {Category.Office})

    # E.g. an address book
    ContactManagement = ("ContactManagement", {Category.Office})

    # Application to manage a database
    Database = ("Database", {Category.Office, Category.Development, Category.AudioVideo})

    # A dictionary
    Dictionary = ("Dictionary", {Category.Office, "TextTools"})

    # Chart application
    Chart = ("Chart", {Category.Office})

    # Email application
    Email = ("Email", {Category.Office, Category.Network})

    # Application to manage your finance
    Finance = ("Finance", {Category.Office})

    # A flowchart application
    FlowChart = ("FlowChart", {Category.Office})

    # Tool to manage your PDA
    PDA = ("PDA", {Category.Office})

    # Project management application
    ProjectManagement = ("ProjectManagement", {Category.Office, Category.Development})

    # Presentation software
    Presentation = ("Presentation", {Category.Office})

    # A spreadsheet
    Spreadsheet = ("Spreadsheet", {Category.Office})

    # A word processor
    WordProcessor = ("WordProcessor", {Category.Office})

    # 2D based graphical application
    _2DGraphics = ("2DGraphics", {Category.Graphics})

    # Application for viewing, creating, or processing vector graphics
    VectorGraphics = ("VectorGraphics", {Category.Graphics, "_2DGraphics"})

    # Application for viewing, creating, or processing raster (bitmap) graphics
    RasterGraphics = ("RasterGraphics", {Category.Graphics, "_2DGraphics"})

    # Application for viewing, creating, or processing 3-D graphics
    _3DGraphics = ("3DGraphics", {Category.Graphics})

    # Tool to scan a file/text
    Scanning = ("Scanning", {Category.Graphics})

    # Optical character recognition application
    OCR = ("OCR", {Category.Graphics, "Scanning"})

    # Camera tools, etc.
    Photography = ("Photography", {Category.Graphics, Category. Office})

    # Desktop Publishing applications and Color Management tools
    Publishing = ("Publishing", {Category.Graphics, Category. Office})

    # Tool to view e.g. a graphic or pdf file
    Viewer = ("Viewer", {Category.Graphics, Category. Office})

    # A text tool utility
    TextTools = ("TextTools", {Category.Utility})

    # Configuration tool for the GUI
    DesktopSettings = ("DesktopSettings", {Category.Settings})

    # A tool to manage hardware components, like sound cards, video cards or printers
    HardwareSettings = ("HardwareSettings", {Category.Settings})

    # A tool to manage printers
    Printing = ("Printing", {"HardwareSettings", Category.Settings})

    # A package manager application
    PackageManager = ("PackageManager", {Category.Settings})

    # A dial-up program
    Dialup = ("Dialup", {Category.Network})

    # An instant messaging client
    InstantMessaging = ("InstantMessaging", {Category.Network})

    # A chat client
    Chat = ("Chat", {Category.Network})

    # An IRC client
    IRCClient = ("IRCClient", {Category.Network})

    # RSS, podcast and other subscription based contents
    Feed = ("Feed", {Category.Network})

    # Tools like FTP or P2P programs
    FileTransfer = ("FileTransfer", {Category.Network})

    # HAM radio software
    HamRadio = ("HamRadio", {Category.Network, Category.Audio})

    # A news reader or a news ticker
    News = ("News", {Category.Network})

    # A P2P program
    P2P = ("P2P", {Category.Network})

    # A tool to remotely manage your PC
    RemoteAccess = ("RemoteAccess", {Category.Network})

    # Telephony via PC
    Telephony = ("Telephony", {Category.Network})

    # Telephony tools, to dial a number, manage PBX, ...
    TelephonyTools = ("TelephonyTools", {Category.Utility})

    # Video Conference software
    VideoConference = ("VideoConference", {Category.Network})

    # A web browser
    WebBrowser = ("WebBrowser", {Category.Network})

    # A tool for web developers
    WebDevelopment = ("WebDevelopment", {Category.Network, Category.Development})

    # An app related to MIDI
    Midi = ("Midi", {Category.AudioVideo, Category.Audio})

    # Just a mixer
    Mixer = ("Mixer", {Category.AudioVideo, Category.Audio})

    # A sequencer
    Sequencer = ("Sequencer", {Category.AudioVideo, Category.Audio})

    # A tuner
    Tuner = ("Tuner", {Category.AudioVideo, Category.Audio})

    # A TV application
    TV = ("TV", {Category.AudioVideo, Category.Video})

    # Application to edit audio/video files
    AudioVideoEditing = ("AudioVideoEditing", {Category.Audio, Category.Video, Category.AudioVideo})

    # Application to play audio/video files
    Player = ("Player", {Category.Audio, Category.Video, Category.AudioVideo})

    # Application to record audio/video files
    Recorder = ("Recorder", {Category.Audio, Category.Video, Category.AudioVideo})

    # Application to burn a disc
    DiscBurning = ("DiscBurning", {Category.AudioVideo})

    # An action game
    ActionGame = ("ActionGame", {Category.Game})

    # Adventure style game
    AdventureGame = ("AdventureGame", {Category.Game})

    # Arcade style game
    ArcadeGame = ("ArcadeGame", {Category.Game})

    # A board game
    BoardGame = ("BoardGame", {Category.Game})

    # Falling blocks game
    BlocksGame = ("BlocksGame", {Category.Game})

    # A card game
    CardGame = ("CardGame", {Category.Game})

    # A game for kids
    KidsGame = ("KidsGame", {Category.Game})

    # Logic games like puzzles, etc
    LogicGame = ("LogicGame", {Category.Game})

    # A role playing game
    RolePlaying = ("RolePlaying", {Category.Game})

    # A shooter game
    Shooter = ("Shooter", {Category.Game})

    # A simulation game
    Simulation = ("Simulation", {Category.Game})

    # A sports game
    SportsGame = ("SportsGame", {Category.Game})

    # A strategy game
    StrategyGame = ("StrategyGame", {Category.Game})

    # Software to teach arts
    Art = ("Art", {Category.Education, Category.Science})

    # No description
    Construction = ("Construction", {Category.Education, Category.Science})

    # Musical software
    Music = ("Music", {Category.AudioVideo, Category.Education})

    # Software to learn foreign languages
    Languages = ("Languages", {Category.Education, Category.Science})

    # Artificial Intelligence software
    ArtificialIntelligence = ("ArtificialIntelligence", {Category.Education, Category.Science})

    # Astronomy software
    Astronomy = ("Astronomy", {Category.Education, Category.Science})

    # Biology software
    Biology = ("Biology", {Category.Education, Category.Science})

    # Chemistry software
    Chemistry = ("Chemistry", {Category.Education, Category.Science})

    # ComputerScience software
    ComputerScience = ("ComputerScience", {Category.Education, Category.Science})

    # Data visualization software
    DataVisualization = ("DataVisualization", {Category.Education, Category.Science})

    # Economy software
    Economy = ("Economy", {Category.Education, Category.Science})

    # Electricity software
    Electricity = ("Electricity", {Category.Education, Category.Science})

    # Geography software
    Geography = ("Geography", {Category.Education, Category.Science})

    # Geology software
    Geology = ("Geology", {Category.Education, Category.Science})

    # Geoscience software, GIS
    Geoscience = ("Geoscience", {Category.Education, Category.Science})

    # History software
    History = ("History", {Category.Education, Category.Science})

    # Software for philosophy, psychology and other humanities
    Humanities = ("Humanities", {Category.Education, Category.Science})

    # Image Processing software
    ImageProcessing = ("ImageProcessing", {Category.Education, Category.Science})

    # Literature software
    Literature = ("Literature", {Category.Education, Category.Science})

    # Software for viewing maps, navigation, mapping, GPS
    Maps = ("Maps", {Category.Education, Category.Science, Category.Utility})

    # Math software
    Math = ("Math", {Category.Education, Category.Science})

    # Numerical analysis software
    NumericalAnalysis = ("NumericalAnalysis", {Category.Education, "Math", Category.Science, "Math"})

    # Medical software
    MedicalSoftware = ("MedicalSoftware", {Category.Education, Category.Science})

    # Physics software
    Physics = ("Physics", {Category.Education, Category.Science})

    # Robotics software
    Robotics = ("Robotics", {Category.Education, Category.Science})

    # Religious and spiritual software, theology
    Spirituality = ("Spirituality", {Category.Education, Category.Science, Category.Utility})

    # Sports software
    Sports = ("Sports", {Category.Education, Category.Science})

    # Parallel computing software
    ParallelComputing = ("ParallelComputing", {Category.Education, "ComputerScience", Category.Science, "ComputerScience"})

    # A simple amusement
    Amusement = ("Amusement", set())

    # A tool to archive/backup data
    Archiving = ("Archiving", {Category.Utility})

    # A tool to manage compressed data/archives
    Compression = ("Compression", {Category.Utility, "Archiving"})

    # Electronics software, e.g. a circuit designer
    Electronics = ("Electronics", set())

    # Emulator of another platform, such as a DOS emulator
    Emulator = ("Emulator", {Category.System, Category.Game})

    # Engineering software, e.g. CAD programs
    Engineering = ("Engineering", set())

    # A file tool utility
    FileTools = ("FileTools", {Category.Utility, Category.System})

    # A file manager
    FileManager = ("FileManager", {Category.System, "FileTools"})

    # A terminal emulator application
    TerminalEmulator = ("TerminalEmulator", {Category.System})

    # A file system tool
    Filesystem = ("Filesystem", {Category.System})

    # Monitor application/applet that monitors some resource or activity
    Monitor = ("Monitor", {Category.System, Category.Network})

    # A security tool
    Security = ("Security", {Category.Settings, Category.System})

    # Accessibility
    Accessibility = ("Accessibility", {Category.Settings, Category.Utility})

    # A calculator
    Calculator = ("Calculator", {Category.Utility})

    # A clock application/applet
    Clock = ("Clock", {Category.Utility})

    # A text editor
    TextEditor = ("TextEditor", {Category.Utility})

    # Help or documentation
    Documentation = ("Documentation", set())

    # Application handles adult or explicit material
    Adult = ("Adult", set())

    # Important application, core to the desktop such as a file manager or a help browser
    Core = ("Core", set())

    # Application based on KDE libraries
    KDE = ("KDE", {"QT"})

    # Application based on GNOME libraries
    GNOME = ("GNOME", {"GTK"})

    # Application based on XFCE libraries
    XFCE = ("XFCE", {"GTK"})

    # Application based on GTK+ libraries
    GTK = ("GTK", set())

    # Application based on Qt libraries
    Qt = ("Qt", set())

    # Application based on Motif libraries
    Motif = ("Motif", set())

    # Application based on Java GUI libraries, such as AWT or Swing
    Java = ("Java", set())

    # Application that only works inside a terminal (text-based or command line application)
    ConsoleOnly = ("ConsoleOnly", set())


def build_category_string(categories, subcategories):
    if Category.Audio in categories or Category.Video in categories:
        logger.debug(f"Adding category {Category.AudioVideo.name}")
        categories.add(Category.AudioVideo)

    extra = {SubCategory.Qt}
    for subcategory in subcategories:
        cats = {i for i in subcategory.value[1] if i in Category}
        subcats = subcategory.value[1] - cats
        extra.update(getattr(SubCategory, i) for i in subcats)
        if cats and not any(i in categories for i in cats):
            raise ValueError(f"To use {subcategory.name} you must include one of {cats}")
    if extra - subcategories:
        logger.debug(f"Adding subcategory {', '.join(i.name for i in extra - subcategories)}")
    subcategories.update(extra)
    return ";".join([i.value for i in categories] + [i.value[0] for i in subcategories])
