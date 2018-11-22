% Lily was here -- automatically converted by /usr/bin/midi2ly from /home/InsMaster/static/files/melody/midi/4615751e-ee24-11e8-8e25-0242ac110002-demons.mp3.mid
\version "2.14.0"

\layout {
  \context {
    \Voice
    \remove "Note_heads_engraver"
    \consists "Completion_heads_engraver"
    \remove "Rest_engraver"
    \consists "Completion_rest_engraver"
  }
}

trackAchannelA = {
  
  \tempo 4 = 120 
  
  \time 4/4 
  
}

trackA = <<
  \context Voice = voiceA \trackAchannelA
>>


trackBchannelB = \relative c {
  r4*28/220 dis''4*197/220 r4*71/220 ais,,,4*14/220 r4*112/220 <ais g' >4*29/220 
  r4*84/220 ais''4*42/220 <ais,, g' >4*28/220 r4*99/220 ais''4*84/220 
  ais4*57/220 <g ais >4*127/220 ais,,4*14/220 r4*56/220 ais''4*197/220 
  <ais,, ais' >4*28/220 r4*42/220 ais''4*71/220 ais,,4*14/220 r4*113/220 ais'4*28/220 
  r4*112/220 ais'4*99/220 ais4*84/220 ais,,4*29/220 r4*28/220 d'4*169/220 
  r4*84/220 c4*141/220 <c g'' >4*141/220 <c, dis >4*14/220 r4*112/220 <c' g'' >4*127/220 
  <g'' g' >4*197/220 c,,,4*71/220 r4*112/220 gis'4*29/220 r4*112/220 <gis gis' >4*141/220 
  <gis c gis' >4*127/220 <gis c gis' >4*140/220 <gis gis' gis' >4*127/220 
  gis' gis c,4*140/220 <c dis dis' g g' >4*127/220 
}

trackBchannelBvoiceB = \relative c {
  r4*28/220 dis'4*268/220 <g, ais ais' >4*126/220 ais4*113/220 
  r4*42/220 ais4*127/220 r4*70/220 dis4*71/220 g,,4*225/220 r4*28/220 <d' d' >4*71/220 
  d4*70/220 ais' r4*71/220 <d, ais' ais' >4*127/220 ais,4*42/220 
  r4*98/220 d'4*197/220 d4*43/220 f4*295/220 r4*99/220 g4*267/220 
  dis4*240/220 r4*14/220 g4*408/220 r4*127/220 gis'4*141/220 gis4*126/220 
  c,,4*381/220 gis'4*267/220 
}

trackBchannelBvoiceC = \relative c {
  r4*28/220 dis4*746/220 dis,4*226/220 r4*169/220 d'4*211/220 f,4*507/220 
  r4*14/220 d'4*267/220 r4*254/220 <c, dis g' >4*126/220 g'4*254/220 
  r4*70/220 <g' g' >4*197/220 r4*268/220 dis,4*282/220 dis4*239/220 
  <dis dis' >4*267/220 
}

trackBchannelBvoiceD = \relative c {
  r4*169/220 ais,4*28/220 r4*99/220 dis''4*478/220 dis,4*310/220 
  r4*155/220 <d ais'' >4*141/220 d'4*521/220 r4*127/220 ais4*140/220 
  r4*254/220 g''4*253/220 c,,,4*254/220 c4*126/220 <c gis'' >4*282/220 
  r4*253/220 dis'4*155/220 r4*183/220 g4*71/220 
}

trackBchannelBvoiceE = \relative c {
  \voiceFour
  r4*169/220 <ais' ais' >4*127/220 r4*126/220 <g ais' >4*155/220 
  g4*268/220 dis'4*281/220 r4*381/220 <d, ais' >4*140/220 dis''4*395/220 
  r4*380/220 <dis, dis' >4*267/220 r4*240/220 c4*140/220 r4*662/220 gis'4*409/220 
}

trackBchannelBvoiceF = \relative c {
  \voiceThree
  r4*436/220 ais'''4*141/220 ais,4*395/220 ais,4*70/220 r4*465/220 ais'4*394/220 
  r4*127/220 c4*492/220 r4*1211/220 gis,,4*521/220 
}

trackBchannelBvoiceG = \relative c {
  r4*436/220 dis,4*155/220 dis4*29/220 r4*154/220 g''4*338/220 
  r4*718/220 ais,,4*71/220 
}

trackBchannelBvoiceH = \relative c {
  \voiceTwo
  r4*859/220 dis''4*98/220 r4*15/220 g,,4*140/220 r4*718/220 ais4*198/220 
}

trackBchannelBvoiceI = \relative c {
  \voiceOne
  r4*972/220 ais''4*267/220 r4*591/220 d4*338/220 
}

trackB = <<

  \clef bass
  
  \context Voice = voiceA \trackBchannelB
  \context Voice = voiceB \trackBchannelBvoiceB
  \context Voice = voiceC \trackBchannelBvoiceC
  \context Voice = voiceD \trackBchannelBvoiceD
  \context Voice = voiceE \trackBchannelBvoiceE
  \context Voice = voiceF \trackBchannelBvoiceF
  \context Voice = voiceG \trackBchannelBvoiceG
  \context Voice = voiceH \trackBchannelBvoiceH
  \context Voice = voiceI \trackBchannelBvoiceI
>>


\score {
  <<
    \context Staff=trackB \trackA
    \context Staff=trackB \trackB
  >>
  \layout {}
  \midi {}
}
