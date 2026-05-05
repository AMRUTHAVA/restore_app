from django.db import migrations

def seed_energy_plan_suggestions(apps, schema_editor):
  # Use apps.get_model instead of importing directly — this gives you
  # the model as it existed at this point in the migration history
  EnergyPlanSuggestion = apps.get_model('restore', 'EnergyPlanSuggestion')

  energy_plan_suggestions = [
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Protect one 60-90 min focus block in your peak window"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Create a no-meeting zone during your best two hours"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Protect your first hour: no reactive work until one priority is done"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Front-load high-focus work to the beginning of your peak"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Schedule one 45-60 min 'decision window' during your peak"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Move one decision-heavy task out of your low window"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"If possible, don't book important decisions in the last third of your day"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Convert one meeting to async (update + decision doc)"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Batch meetings into one block instead of spreading them"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Break up any 2+ hour meeting streak with one 10-min buffer"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Move one recurring meeting out of your low window"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Add a 15-min buffer after your densest block"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Put a 20-30 min break before any late-afternoon meetings"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Block 30 minutes after your busiest block for follow-ups"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Break long meeting streaks with a 10-min reset"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Put admin/email in low-energy time"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Save creative work for peak"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Move one recurring meeting out of your low window"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Move decision-heavy work out of low window"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Protect first hour from email/DMs"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Block 30 min for follow-ups so they don't spill all day"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Batch meetings instead of scattering them"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Pick one clear priority task to work on in your peak window"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Prep before high-stakes meetings (goal, decision, ask)"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Skim next agendas in a meeting-heavy block and note decisions"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Reorder tasks inside a fixed block (hard -> easy)"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Lower the bar during your low window (admin/logistics)"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Use 'good enough' for low-stakes work; save precision for peak"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Pick one clear priority for peak"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Batch quick email replies into two short bursts"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Pick one rule for the day (e.g., check email at 11 & 4)"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Turn on Do Not Disturb for 25 minutes"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Open necessary docs before meeting streaks"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Tighten meetings: request agenda or suggest 25-minute format"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"If a meeting has no decision, ask for desired outcome in minute one"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"End meetings with one next step + owner"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Prep before high-stakes meetings"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Skim agendas and identify decisions"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Choose one energy-saver today (same breakfast, template, routine)"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Pick one rule for the day"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Use 'good enough' instead of perfection"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Lower the bar during low window"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Take 60 seconds between blocks to reset"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Open materials before meeting streaks to reduce stress buildup"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Parasympathetic Downshift",
        "suggestion_text":"2-minute slow exhales (longer exhale than inhale)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Parasympathetic Downshift",
        "suggestion_text":"Box breathing for 90 seconds (4-4-4-4)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Parasympathetic Downshift",
        "suggestion_text":"1-minute posture reset with slow exhale"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Muscular Release",
        "suggestion_text":"60-second shoulder/neck release + un-clench jaw"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Muscular Release",
        "suggestion_text":"2-minute stretch (hamstrings + chest open)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Muscular Release",
        "suggestion_text":"Legs elevated for 2 minutes"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Muscular Release",
        "suggestion_text":"1-minute posture reset"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Light/Circadian Cue",
        "suggestion_text":"90 seconds of daylight"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Light/Circadian Cue",
        "suggestion_text":"30-second eye break (distance focus + blink)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Light/Circadian Cue",
        "suggestion_text":"60-second nature reset (bird sounds, wind, trees)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"2-minute walk"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"1-minute water reset (drink + stand)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"Elevate your legs or change your position"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"3-2-1 grounding (see/hear/feel)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"60-second gratitude/grounding"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"60-second nature listening reset"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"90-second 'handoff' (close tabs + write what's next)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"2-minute music reset (one song, no multitasking)"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"30-second eye break"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Cut or decline one meeting that no longer fits"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Do not begin a new project in the last 90 minutes of work"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Use your peak window for output only no reading or reviewing"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Block 'thinking time' as a non-negotiable calendar appointment"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Log non-urgent decisions in a weekly 'decisions inbox'"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"No same-day decisions on anything that can wait"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Pre-decide tomorrow's task order so mornings start decision-free"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Delegate one recurring decision and formalize it in writing"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Make Friday afternoons meeting-free as the standard"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Shorten default meetings: 60->45 min, 30->20 min"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Schedule a 30-minute transition block between morning and afternoon"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Protect the 60 minutes before your most critical meeting"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"End each day: Find a stopping place in a task and set tomorrow's top task"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Strategic Buffering",
        "suggestion_text":"Hold one unscheduled 'recovery hour' weekly for any outstanding tasks"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Map your three critical tasks to your three peak windows"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Eliminate, automate, or delegate low-cognition tasks"
    },
    {
        "tier":"A",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Tell your team your prefered communication hours"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Before a focus block, write the one output you want"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Close all unrelated tabs before starting a work block"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Set a timer you can see to anchor a 25-minute sprint"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Focus Protection",
        "suggestion_text":"Set a specific stop time before you start working"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"In meetings, log non-urgent items in a 'later' list"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"One-touch rule: low-stakes decisions get made once, never revisited"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Before key meetings, write down your goal for the main item"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Decision Containment",
        "suggestion_text":"Put today's one critical decision in your peak window"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Arrive at the next meeting with one question already prepared"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Take notes in one recurring meeting to force structure"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Meeting Restructure",
        "suggestion_text":"Can't shorten a meeting? Spend 5 minutes prepping beforehand"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Pre-assign low-energy hours to email, filing, and admin"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"When energy dips, switch from deep work to shallow tasks"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Keep 3 low-lift tasks ready for when energy drops"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Front-load creative tasks; push reading and review to later"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Mute non-essential notifications; check twice daily, not constantly"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Wait 10 minutes before replying to any non-urgent message"
    },
    {
        "tier":"B",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"After each task, write down exactly where you left off"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"Write down the one thing you must finish today"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"Clear mental clutter: write all pending tasks in 60 seconds"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Cognitive Grounding",
        "suggestion_text":"To regain focus, label what you're feeling right now in one word"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"Before switching tasks, state the next task out loud"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"Mark each finished task visibly done checkmark or strikethrough"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"Sit-to-stand (or reverse) to signal a new work mode"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Transition Ritual",
        "suggestion_text":"At midday, restate your single afternoon priority out loud"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"Stand and take 10 slow steps to re-engage alertness"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"Roll shoulders back and drop resets posture instantly"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"Press feet into floor for 5 seconds to sharpen focus"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Movement Reset",
        "suggestion_text":"Shake out your hands 10 seconds to release typing tension"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Light/Circadian Cue",
        "suggestion_text":"Raise screen brightness slightly during your afternoon low"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Light/Circadian Cue",
        "suggestion_text":"Look out a window for 60 seconds to reset fatigue"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Hit a wall? Switch to reading. A different energy is required"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Keep a 'quick wins' list this reinforces daily momentum"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Can't focus? Work on anything adjacent to your main task"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Energy-Task Matching",
        "suggestion_text":"Switch to handwriting for 3 minutes when thinking feels stuck"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Set your mobile device status to do not disturb during deep work"
    },
    {
        "tier":"C",
        "behavioral_cluster":"Reactive Containment",
        "suggestion_text":"Before checking recent notifcations, write down what you were doing"
    }
]

  for energy_plan_suggestion in energy_plan_suggestions:
    EnergyPlanSuggestion.objects.create(**energy_plan_suggestion)

def reverse_seed(apps, schema_editor):
  EnergyPlanSuggestion = apps.get_model('restore', 'EnergyPlanSuggestion')
  EnergyPlanSuggestion.objects.all().delete()

class Migration(migrations.Migration):
  initial = True
  
  dependencies = [
    ('restore', '0009_create_energy_plan_suggestions'),
  ]

  operations = [
    migrations.RunPython(seed_energy_plan_suggestions, reverse_seed),
  ]