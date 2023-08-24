(ros::roseus-add-msgs "soft_exterior_hand")
(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(ros::advertise "/servo_states" soft_exterior_hand::UInt16Array 1)

;;腕が上向き
(send *aero* :angle-vector #f(-13.97 -9.968 -17.01 -135.1 0.0 0.0 0.0 -0.05 -4.98 9.97 19.98 -120.0 -89.0 4.98 20.0 0.0 0.0 24.94 -0.013 0.0 0.0 0.0 42.4 -60.9 -42.4 60.9))
(send *ri* :angle-vector (send *aero* :angle-vector) 2000)
(send *ri* :wait-interpolation)

;;ロボットが手を開く
(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 160 30 180 270))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 0.8)
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
    (ros::duration-sleep 0.5)
    )
)

;;ロボットがセンサを見ながら手を閉じる
(setq cnt 0)
(setq deg 270)
(while (< cnt 2)
  (setq cnt 0)
  (let ((sensor-states (one-shot-subscribe "/sensor_states" soft_exterior_hand::UInt16Array :timeout 20000)))
    (setq data (send sensor-states :data))
    (dotimes (i 14)
      (when (> (elt data i) 10)
        (setq cnt (+ cnt 1))))
    (setq deg (- deg 30))
    (send pub-msg :data (integer-vector 80 107 128 120 90 30 180 deg))
    (ros::publish "/servo_states" pub-msg)
    (ros::duration-sleep 0.5)
))



