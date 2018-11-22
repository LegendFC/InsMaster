% Lily was here -- automatically converted by /usr/bin/midi2ly from /home/InsMaster/static/files/melody/midi/4882ea84-ee24-11e8-9c8d-0242ac110002-cloud.m4a.mid
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
  r4*113/220 <ais, b >4*14/220 r4*422/220 a4*28/220 r4*211/220 b4*15/220 
  r4*169/220 ais4*28/220 r4*14/220 ais4*28/220 r4*436/220 e'''4*479/220 
  dis4*239/220 r4*127/220 ais,,4*14/220 r4*57/220 b4*28/220 ais 
  r4*197/220 a4*14/220 r4*85/220 <g' ais >4*14/220 r4*155/220 b,4*28/220 
  r4*112/220 b4*14/220 r4*57/220 b4*42/220 r4*141/220 b4*42/220 
  r4*14/220 dis''4*197/220 r4*42/220 a,4*29/220 r4*197/220 g,4*28/220 
  r4*183/220 b4*14/220 r4*225/220 a4*28/220 r4*212/220 fis'''4*352/220 
  r4*98/220 e,4*57/220 r4*183/220 a, r4*28/220 b,4*141/220 r4*112/220 dis''4*113/220 
  r4*28/220 b,4*183/220 r4*28/220 b,4*14/220 r4*99/220 a4*14/220 
  r4*70/220 e'4*43/220 r4*112/220 b4*14/220 r4*212/220 gis4*28/220 
  r4*197/220 b''4*253/220 r4*211/220 b4*15/220 r4*436/220 a,,4*28/220 
  r4*197/220 <a a' >4*28/220 r4*198/220 b''4*478/220 a,,4*226/220 
  ais4*28/220 r4*225/220 <ais b >4*28/220 r4*197/220 a'4*169/220 
  r4*282/220 b,4*211/220 b4*169/220 b4*84/220 ais4*29/220 r4*211/220 <gis b >4*14/220 
  r4*155/220 e'''4*169/220 
}

trackBchannelBvoiceB = \relative c {
  \voiceTwo
  r4*549/220 e'4*254/220 r4*169/220 a,,,4*84/220 r4*521/220 b''4*239/220 
  r4*127/220 b,,4*239/220 b4*14/220 r4*127/220 <b e'' >4*71/220 
  r4*14/220 fis''4*521/220 r4*197/220 ais,,4*225/220 r4*28/220 a4*14/220 
  r4*211/220 e'''4*240/220 r4*436/220 a,,4*183/220 r4*141/220 e'4*14/220 
  r4*14/220 e4*85/220 r4*28/220 b,4*14/220 cis''4*127/220 r4*324/220 a,,4*239/220 
  r4*225/220 b4*155/220 b4*71/220 a4*14/220 gis r4*98/220 fis''4*127/220 
  r4*70/220 b4*282/220 r4*99/220 b,,4*563/220 r4*126/220 b'''4*578/220 
  r4*98/220 e,4*240/220 r4*225/220 a,,4*28/220 r4*197/220 b,4*14/220 
  r4*226/220 cis''4*197/220 r4*281/220 a,,4*197/220 r4*268/220 cis4*14/220 
  r4*197/220 <ais fis'' >4*14/220 r4*141/220 fis''4*99/220 r4*225/220 e'4*169/220 
  r4*112/220 b,,4*43/220 
}

trackBchannelBvoiceC = \relative c {
  \voiceFour
  r4*788/220 fis4*57/220 r4*169/220 cis'4*577/220 r4*99/220 b,,4*14/220 
  r4*464/220 fis''4*240/220 r4*14/220 b,,4*183/220 r4*42/220 a'4*28/220 
  r4*71/220 ais,4*28/220 r4*141/220 ais4*211/220 r4*14/220 gis''4*183/220 
  r4*56/220 ais,,4*42/220 r4*409/220 b'''4*225/220 r4*225/220 e,4*254/220 
  r4*155/220 e4*28/220 r4*28/220 a,,,4*465/220 e'''4*478/220 fis,4*14/220 
  r4*198/220 b,,4*28/220 r4*211/220 fis'''4*1577/220 r4*28/220 fis4*253/220 
  r4*437/220 e4*239/220 r4*226/220 a,,,4*478/220 e'''4*240/220 
  r4*225/220 dis r4*225/220 b,,4*127/220 
}

trackBchannelBvoiceD = \relative c {
  \voiceThree
  r4*788/220 fis'4*1141/220 r4*253/220 e4*141/220 r4*99/220 fis4*718/220 
  r4*239/220 b,,,4*141/220 
  | % 5
  r4*1816/220 b''4*310/220 r4*254/220 fis4*126/220 r4*352/220 gis'4*437/220 
  r4*253/220 gis4*240/220 r4*1140/220 a,,,4*14/220 r4*197/220 ais4*28/220 
  r4*817/220 b''4*211/220 r4*338/220 e4*254/220 
}

trackBchannelBvoiceE = \relative c {
  \voiceOne
  r4*2647/220 e'4*197/220 r4*3056/220 e4*267/220 r4*2492/220 fis4*535/220 
  r4*1098/220 fis8*5 
}

trackB = <<

  \clef bass
  
  \context Voice = voiceA \trackBchannelB
  \context Voice = voiceB \trackBchannelBvoiceB
  \context Voice = voiceC \trackBchannelBvoiceC
  \context Voice = voiceD \trackBchannelBvoiceD
  \context Voice = voiceE \trackBchannelBvoiceE
>>


\score {
  <<
    \context Staff=trackB \trackA
    \context Staff=trackB \trackB
  >>
  \layout {}
  \midi {}
}
