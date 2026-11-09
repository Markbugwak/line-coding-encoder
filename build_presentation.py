"""Generate the eight-slide line-coding presentation, including speaker notes."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
NAVY=RGBColor(18,31,52); BLUE=RGBColor(43,103,176); LIGHT=RGBColor(239,244,250)
DARK=RGBColor(35,43,55); YELLOW=RGBColor(255,220,80); WHITE=RGBColor(255,255,255)
MUTED=RGBColor(95,108,125)

def slide(title, subtitle, bullets, notes, number, dark=False):
    s=prs.slides.add_slide(prs.slide_layouts[6])
    bg=s.background.fill; bg.solid(); bg.fore_color.rgb=NAVY if dark else WHITE
    if dark:
        title_box=s.shapes.add_textbox(Inches(.9), Inches(1.6), Inches(11.7), Inches(1.2))
        p=title_box.text_frame.paragraphs[0]; p.text=title; p.font.size=Pt(36); p.font.bold=True; p.font.color.rgb=WHITE
        sub=s.shapes.add_textbox(Inches(.95), Inches(3.0), Inches(11.4), Inches(.8))
        p=sub.text_frame.paragraphs[0]; p.text=subtitle; p.font.size=Pt(25); p.font.color.rgb=RGBColor(174,203,237)
        foot=s.shapes.add_textbox(Inches(.95), Inches(5.7), Inches(11.4), Inches(.5))
        p=foot.text_frame.paragraphs[0]; p.text="Stallings • Data and Computer Communications • Section 5.1"; p.font.size=Pt(15); p.font.color.rgb=WHITE
    else:
        tb=s.shapes.add_textbox(Inches(.65), Inches(.35), Inches(12), Inches(.65))
        p=tb.text_frame.paragraphs[0]; p.text=title; p.font.size=Pt(29); p.font.bold=True; p.font.color.rgb=NAVY
        st=s.shapes.add_textbox(Inches(.68), Inches(1.05), Inches(12), Inches(.42))
        p=st.text_frame.paragraphs[0]; p.text=subtitle; p.font.size=Pt(13); p.font.color.rgb=MUTED
        box=s.shapes.add_textbox(Inches(.9), Inches(1.65), Inches(11.5), Inches(4.9))
        tf=box.text_frame; tf.word_wrap=True
        for i,item in enumerate(bullets):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
            p.text=item; p.level=0; p.font.size=Pt(20); p.font.color.rgb=DARK; p.space_after=Pt(16); p.bullet=True
    n=s.shapes.add_textbox(Inches(12.15), Inches(7.08), Inches(.55), Inches(.22))
    p=n.text_frame.paragraphs[0]; p.text=f"{number}/8"; p.font.size=Pt(10); p.font.color.rgb=WHITE if dark else MUTED
    s.notes_slide.notes_text_frame.text=notes
    return s

slide("LINE CODING TECHNIQUES","Digital Data → Digital Signals",[],
      "Introduce the topic. Line coding converts binary bits into electrical signal levels for transmission. This presentation reviews the eight techniques implemented in the project.",1,True)
slide("What is line coding?","Representing binary data as signal levels over time.",[
"The input is a sequence of bits, such as 01001100011.",
"The encoder maps each bit to one or more voltage levels.",
"The receiver observes signal changes and recovers the original data.",
"Different schemes balance synchronization, bandwidth, and error behavior."
],"Define digital data and digital signal. A bit carries information; the waveform is its physical representation. No single coding scheme is best in every situation.",2)
slide("NRZ and bipolar schemes","These methods usually use one signal level for each bit.",[
"NRZ-L: 0 is high (+V); 1 is low (−V).",
"NRZI: a 1 causes a transition at the beginning of the bit; a 0 does not.",
"Bipolar-AMI: each 1 alternates between +V and −V; each 0 is zero voltage.",
"Pseudoternary: each 0 alternates between +V and −V; each 1 is zero voltage."
],"Explain the four schemes. These are the project's conventions: NRZ-L maps 0 to high and 1 to low. NRZI changes at the start of a 1. AMI alternates 1 pulses; pseudoternary alternates 0 pulses.",3)
slide("Biphase schemes","Two half-bit signal levels are produced for every input bit.",[
"Manchester: every bit has a transition in the middle.",
"A 1 is low-to-high; a 0 is high-to-low.",
"Differential Manchester: every bit has a middle transition.",
"In Differential Manchester, a 0 also has a transition at the start of the bit."
],"The mid-bit transition helps the receiver keep timing. Manchester uses low-to-high for 1 and high-to-low for 0. Differential Manchester always changes in the middle, and a 0 has an additional start transition.",4)
s=slide("B8ZS substitution","Eight consecutive zeros are replaced with a transition-rich pattern.",[
"B8ZS is based on Bipolar-AMI.",
"A run of eight zeros is replaced by 000VB0VB.",
"V means a bipolar violation; B means a normal bipolar pulse.",
"The substitution avoids a long flat zero-voltage interval."
],"B8ZS is AMI-based. Eight consecutive zeros become 000VB0VB. V is a deliberate violation of AMI alternation; B is a normal bipolar pulse. The yellow label below highlights the substitution.",5)
chip=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1), Inches(5.7), Inches(6.5), Inches(.7))
chip.fill.solid(); chip.fill.fore_color.rgb=YELLOW; chip.line.color.rgb=YELLOW; chip.text_frame.vertical_anchor=MSO_ANCHOR.MIDDLE
p=chip.text_frame.paragraphs[0]; p.text="000 V B 0 V B"; p.alignment=PP_ALIGN.CENTER; p.font.size=Pt(24); p.font.bold=True; p.font.color.rgb=NAVY
s=slide("HDB3 substitution","Four consecutive zeros are replaced according to the pulse count.",[
"HDB3 is also based on Bipolar-AMI.",
"If the number of pulses since the last substitution is odd, use 000V.",
"If the number of pulses is even, use B00V.",
"The rule limits long runs with no signal transitions."
],"Count nonzero pulses since the previous substitution. An odd count produces 000V. An even count produces B00V. In this project the count begins at zero (even), and the initial AMI pulse polarity is negative.",6)
for x,label in [(1.0,"000V  •  odd pulse count"),(6.8,"B00V  •  even pulse count")]:
    chip=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(5.7), Inches(5.3), Inches(.7))
    chip.fill.solid(); chip.fill.fore_color.rgb=YELLOW; chip.line.color.rgb=YELLOW; chip.text_frame.vertical_anchor=MSO_ANCHOR.MIDDLE
    p=chip.text_frame.paragraphs[0]; p.text=label; p.alignment=PP_ALIGN.CENTER; p.font.size=Pt(17); p.font.bold=True; p.font.color.rgb=NAVY
s=slide("Quick comparison","General characteristics; actual performance depends on the link and implementation.",[
"NRZ-L / NRZI — simple and bandwidth-efficient; long runs can challenge clock recovery and may contain DC.",
"AMI / Pseudoternary — three signal levels and reduced DC content; long zero/no-pulse runs need attention.",
"Manchester — strong self-clocking and balanced signal; requires more bandwidth.",
"Differential Manchester — self-clocking and transition-based; requires more bandwidth.",
"B8ZS / HDB3 — AMI-based substitutions add transitions during long zero runs."
],"Compare the schemes as general tendencies, not absolute guarantees for every physical system. NRZ is simple but long runs can challenge timing and can carry DC. AMI-family schemes reduce DC; Manchester-family schemes provide regular transitions but use more bandwidth.",7)
slide("Project summary and demo","Eight schemes • text output • waveform plots",[
"Enter a bit string in the interactive menu or use CLI mode.",
"CLI example: python encoding_techniques.py 01001100011",
"Signal levels are printed as +, 0, and −.",
"Waveform plots highlight B8ZS and HDB3 substitutions in yellow.",
"Automated tests check sample outputs and substitution cases."
],"Close by demonstrating the sample command. CLI prints encoded levels; the interactive menu can also draw waveforms. Tests protect the project's current encoding conventions from accidental changes.",8)
prs.save("presentation.pptx")
print("Created presentation.pptx (8 slides with speaker notes).")
