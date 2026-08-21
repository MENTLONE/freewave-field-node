# FreeWave Signal Society Field Node
## Field Deployment Checklist

Use this checklist before transporting or deploying the FreeWave Field Node.

---

## 1. Physical Inspection

- [ ] Pelican case is intact
- [ ] 3D-printed holding bracket is secure
- [ ] Raspberry Pi is secured
- [ ] Heltec V4 is secured
- [ ] Touchscreen is secured
- [ ] USB connections are secure
- [ ] DSI display cable is secure
- [ ] No loose components inside the enclosure
- [ ] No damaged cables
- [ ] Case closes without putting pressure on electronics

---

## 2. Power

- [ ] Power bank fully charged
- [ ] Raspberry Pi power cable connected
- [ ] Power bank output is sufficient for the Raspberry Pi
- [ ] Heltec USB connection is secure
- [ ] Spare USB cable available if needed
- [ ] Backup power bank available if required

---

## 3. Raspberry Pi

- [ ] Raspberry Pi boots normally
- [ ] FreeWave splash screen appears
- [ ] FreeWave interface launches
- [ ] Touchscreen responds
- [ ] Keyboard input works if connected
- [ ] System status is visible
- [ ] No obvious error messages

---

## 4. Meshtastic Radio

- [ ] Heltec WiFi LoRa 32 V4 is powered
- [ ] Heltec is connected to Raspberry Pi by USB
- [ ] Radio serial connection is established
- [ ] Meshtastic interface is active
- [ ] Local node information is visible

Check the serial device if necessary:

    ls /dev/ttyACM*

The current configuration expects:

    /dev/ttyACM0

---

## 5. Mesh Network

- [ ] Remote nodes appear in the node list
- [ ] Node information is updating
- [ ] Mesh activity is visible
- [ ] Public messages can be viewed
- [ ] Direct messages can be viewed
- [ ] Direct node selection works
- [ ] Message transmission works

---

## 6. Touchscreen

Test the primary touchscreen controls:

- [ ] Node selection
- [ ] Message navigation
- [ ] Channel navigation
- [ ] Direct-message controls
- [ ] Send controls
- [ ] Power/system controls
- [ ] Scrolling/navigation

---

## 7. Automatic Startup

Verify the FreeWave service:

    sudo systemctl status freewave-field-node --no-pager

Expected:

    Active: active (running)

Verify automatic startup:

    sudo systemctl is-enabled freewave-field-node

Expected:

    enabled

---

## 8. Final Reboot Test

Before field deployment, perform a complete reboot test:

    sudo reboot

After reboot verify:

1. Raspberry Pi boots
2. FreeWave splash appears
3. FreeWave interface launches
4. Touchscreen responds
5. Heltec radio connects
6. Mesh nodes appear
7. Messaging functions correctly

---

## 9. Presentation Mode

For demonstrations and Pub Talks presentations:

- [ ] Display is clean and readable
- [ ] FreeWave splash is working
- [ ] Node list contains visible mesh activity
- [ ] Messaging demonstration is prepared
- [ ] Touchscreen is responsive
- [ ] Power bank is charged
- [ ] Enclosure is clean
- [ ] All cables are secured

---

## 10. Field Deployment

Before leaving with the node:

- [ ] Power bank charged
- [ ] Backup power available
- [ ] USB cable packed
- [ ] Keyboard packed if required
- [ ] Spare microSD card available if required
- [ ] Case securely closed
- [ ] Node physically protected
- [ ] GitHub repository is up to date
- [ ] Current known-good software version confirmed

Check the current Git state:

    git status

Check the current software version:

    git log -1 --oneline

---

## 11. Known-Good Baseline

The presentation-ready FreeWave Field Node baseline is:

**Milestone 9 — Touchscreen UI and FreeWave presentation mode**

The known-good software should be treated as the recovery baseline.

Do not modify the production node immediately before a field deployment unless
the change has been tested and committed.

---

## FreeWave Signal Society

**Chicago Division**

Portable Meshtastic field communications.

Build it.  
Replicate it.  
Take it into the field.
