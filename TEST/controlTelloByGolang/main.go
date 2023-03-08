package main

import (
    "fmt"
    "os/exec"
    "time"

    "gobot.io/x/gobot"
    "gobot.io/x/gobot/platforms/keyboard"
    "gobot.io/x/gobot/platforms/dji/tello"
)

func main() {
    drone := tello.NewDriver("8890")
    keys := keyboard.NewDriver()

    work := func() {
        /**
        ドローンカメラアクセス
        */
        mplayer := exec.Command("mplayer", "-fps", "25", "-")
        mplayerIn, _ := mplayer.StdinPipe()
        if err := mplayer.Start(); err != nil {
            fmt.Println(err)
            return
        }

        drone.On(tello.ConnectedEvent, func(data interface{}) {
            fmt.Println("Connected")
            drone.StartVideo()
            drone.SetVideoEncoderRate(4)
            gobot.Every(100*time.Millisecond, func() {
                drone.StartVideo()
            })
        })

        drone.On(tello.VideoFrameEvent, func(data interface{}) {
            pkt := data.([]byte)
            if _, err := mplayerIn.Write(pkt); err != nil {
                fmt.Println(err)
            }
        })

        /**
        ドローン制御
        */
        keys.On(keyboard.Key, func(data interface{}) {
            key := data.(keyboard.KeyEvent)

            if key.Key == keyboard.C {
                fmt.Println("Command Test")
            } else if key.Key == keyboard.T{
                fmt.Println("Take Off!")
                drone.TakeOff() //離陸
            } else if key.Key == keyboard.L{
                fmt.Println("Land")
                // drone.TakeLand() //着陸
				drone.Land()
            } else if key.Key == keyboard.ArrowUp{
                fmt.Println("↑")
                drone.Forward(10) //前進
            } else if key.Key == keyboard.ArrowDown{
                fmt.Println("↓")
                drone.Backward(10) //後退
            } else if key.Key == keyboard.ArrowRight{
                fmt.Println("→")
                drone.Right(10) //右へ
            } else if key.Key == keyboard.ArrowLeft{
                fmt.Println("←")
                drone.Left(10) //左へ
            } else if key.Key == keyboard.U{
                fmt.Println("Up")
                drone.Up(10) //上昇
            } else if key.Key == keyboard.D{
                fmt.Println("Down")
                drone.Down(10) //下降
            } else if key.Key == keyboard.F{
                fmt.Println("Front Flip")
                drone.FrontFlip() //フリップ
            } else if key.Key == keyboard.B{
                fmt.Println("Back Flip")
                drone.BackFlip() //バックフリップ
            } else {
                fmt.Println("keyboard event!", key, key.Char)
            }
        })
    }

    robot := gobot.NewRobot("tello",
        []gobot.Connection{},
        []gobot.Device{drone, keys}, //droneとkeysの二つのアダプタ
        work,
    )

    robot.Start()
}