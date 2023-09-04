(ros::roseus-add-msgs "soft_exterior_hand")
(load "package://aeroeus/aero-interface.l")
(aero-init)
(send *aero* :angle-vector (send *ri* :state :potentio-vector))

(ros::advertise "/servo_states" soft_exterior_hand::UInt16Array 1)

(send *aero* :angle-vector #f(-13.9589 -9.94925 -16.98 -135.148 0.0 0.0 0.0 -0.04 -17.827 11.3199 -5.28 -68.4346 -30.39 0.0 4.54331 0.0 0.0 24.8837 0.012987 5.02 13.0844 0.0 42.0302 -48.1696 -42.0324 48.1751))
(send *ri* :angle-vector (send *aero* :angle-vector) 4000)
(send *ri* :wait-interpolation)
(send *aero* :inverse-kinematics                                             (send (send *aero* :larm :end-coords :copy-worldcoords)                      :translate (float-vector 0 0 -60) :world)
        :ik-group :larm-whole-body                                                        :rotation-axis t                                                       :revert-if-fail t)
  (send *ri* :angle-vector (send *aero* :angle-vector) 100)
  (send *ri* :wait-interpolation)

(setq pub-msg (instance soft_exterior_hand::UInt16Array :init))
(send pub-msg :data #i(80 107 128 120 60 30 180 30))
(ros::publish "/servo_states" pub-msg)
(ros::duration-sleep 1.0)

(send *aero* :inverse-kinematics                                             (send (send *aero* :larm :end-coords :copy-worldcoords)                      :translate (float-vector 0 0 60) :world)
        :ik-group :larm-whole-body                                                        :rotation-axis t                                                       :revert-if-fail t)
  (send *ri* :angle-vector (send *aero* :angle-vector) 100)
  (send *ri* :wait-interpolation)

