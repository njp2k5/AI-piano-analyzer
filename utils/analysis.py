import pretty_midi
from music21 import converter, analysis, note, chord, stream
import streamlit as st

def analyze_midi(path):
    pm = pretty_midi.PrettyMIDI(path)
    
    # detects key and key signature using music21
    score = converter.parse(path)
    key = score.analyze('key')
    key_signature = f"{key.tonic.name} {key.mode}"

    # computes average loudness as the mean of all notes across all instruments on the music score 
    velocities = [n.velocity for inst in pm.instruments for n in inst.notes]
    avg_vel = round(sum(velocities) / len(velocities)) if velocities else 0

   # inspects tempo property of midi file if unavailabe, it is computed 
    _,tempi = pm.get_tempo_changes()
    if len(tempi) > 0:
        tempo = round(tempi[0])  
    else:
        tempo = round(pm.estimate_tempo()) 

    # computes note density by dividing total number of notes by duration
    total_duration = pm.get_end_time()
    piano = pm.instruments[0] 
    note_count = len(piano.notes)
    note_density = round(note_count / total_duration, 2)

    return {
        "key": key_signature,
        "tempo": tempo,
        "avg_velocity": avg_vel,
        "duration" : total_duration,
        "note_count" : note_count,
        "note_density": note_density
    }

def display_feedback(results):
    st.header("🎧 AI Feedback")
    
    st.subheader("🎼 Musical Key")
    st.write(f"Detected key: **{results['key']}**")

    st.subheader("⏱️ Tempo")
    st.write(f"Estimated tempo: **{results['tempo']} BPM**")
    if results['tempo'] < 60:
        st.info("lower tempo means exposed notes note it")
    elif results['tempo'] > 120:
        st.info("Your tempo is quite fast — keep control!")
    else:
        st.info("good job on the tempo")

    st.subheader("🎹 Dynamics")
    st.write(f"Average note velocity: **{results['avg_velocity']}**")
    if results['avg_velocity'] < 40:
        st.info("faint dynamics ! Try playing with more force for dynamic expression.")
    elif results['avg_velocity'] > 100:
        st.info("Good energy! But ensure you also use soft notes.")
    else:
        st.info("just the sweet spot for dynamics")

    st.subheader("🧠 Note Density")
    st.write(f"total duration of score: {results['duration']}")
    st.write(f"total notes in score: {results['note_count']}")
    st.write(f"Notes per second: **{results['note_density']}**")
    if results['note_density'] < 1:
        st.info("The piece feels sparse. Try adding more fill to the piece.")
    elif results['note_density'] > 3:
        st.info("This is a dense performance — be sure it's intentional.")
    else:
        st.info("good balance of density")
