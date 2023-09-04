(ros::roseus-add-msgs "soft_exterior_hand")
(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(ros::advertise "/servo_states" soft_exterior_hand::UInt16Array 1)

;;腕が下向き
(send *aero* :angle-vector #f(-14.0 -10.0 -17.0 -135.0 0.0 0.0 0.0 0.0 9.2 8.94 20.32 -79.0 89.0 4.98 -10.256 -3.37 0.0 25.0 0.0 0.0 0.0 0.0 21.7 -34.7 -21.7 34.7))
(send *ri* :angle-vector (send *aero* :angle-vector) 2000)
(send *ri* :wait-interpolation)

;;ロボットが手を開く
(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 160 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 0.4)
(send pub-msg :data #i(80 107 128 120 90 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 1.0)

;;センサをみる
(setq cnt 0)
(while (< cnt 1)
  (setq cnt 0)
  (let ((sensor-states (one-shot-subscribe "/sensor_states" soft_exterior_hand::UInt16Array :timeout 20000)))
    (setq data (send sensor-states :data))
    (dotimes (i 14)
      (when (> (elt data i) 10)
        (setq cnt (+ cnt 1))))
    ;; (ros::duration-sleep 0.5)
    )
  (format t "~A" cnt)
  (send *aero* :inverse-kinematics                                             (send (send *aero* :larm :end-coords :copy-worldcoords)                      :translate (float-vector 8 0 0))
        :ik-group :larm                                                        :rotation-axis t                                                       :revert-if-fail nil)
  (send *ri* :angle-vector (send *aero* :angle-vector) 100)
  (send *ri* :wait-interpolation)
)

;;ロボットがセンサを見ながら手を閉じる
(setq cnt 0)
(setq deg 270)
(while (< cnt 2)
  (setq cnt 0)
  (let ((sensor-states (one-shot-subscribe "/sensor_states" soft_exterior_hand::UInt16Array :timeout 20000)))
    (setq data (send sensor-states :data))
    (when (> (elt data 2) 10)
        (setq cnt (+ cnt 1)))
    (when (> (elt data 5) 10)
      (setq cnt (+ cnt 1)))
    (when (> (elt data 8) 10)
        (setq cnt (+ cnt 1)))
    (when (> (elt data 11) 10)
        (setq cnt (+ cnt 1)))
    (setq deg (- deg 30))
    (when (< deg 20)
      (exit))
    (send pub-msg :data (integer-vector 80 107 128 120 90 30 180 deg))
    (ros::publish "/servo_states" pub-msg)
    (ros::duration-sleep 0.3)
))

(ros::duration-sleep 2.0)
(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 160 30 0 270))
(ros::publish "/servo_states" pub-msg
)



