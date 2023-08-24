(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(send *aero* :angle-vector #f(-14.0 -10.0 -17.0 -135.0 0.0 0.0 0.0 0.0 9.2 8.94 20.32 -79.0 -75.1 4.985 -10.256 -3.37 0.0 25.0 0.0 0.0 0.0 0.0 21.7 -34.7 -21.7 34.7))
(send *ri* :angle-vector (send *aero* :angle-vector) 2000)
(send *ri* :wait-interpolation)

;;ロボットが手を開く

;;センサをみる

;;loop
;; (send *aero* :inverse-kinematics                                                       
;;       (send (send *aero* :larm :end-coords :copy-worldcoords)                                          
;;             :translate (float-vector 5 0 0))
;;       :ik-group :larm                                                                                  
;;       :rotation-axis t                                                                                 
;;       :revert-if-fail nil)
;; (send *ri* :angle-vector (send *aero* :angle-vector) 100)

;;ロボットがセンサを見ながら手を閉じる


