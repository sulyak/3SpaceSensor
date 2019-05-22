using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;
using System;

/// <summary>
///     Example of requester who only sends Hello. Very nice guy.
///     You can copy this class and modify Run() to suits your needs.
///     To use this class, you just instantiate, call Start() when you want to start and Stop() when you want to stop.
/// </summary>
public class Requester : RunAbleThread
{
    public string trueMessage;
    /// <summary>
    ///     Request Hello message to server and receive message back. Do it 10 times.
    ///     Stop requesting when Running=false.
    /// </summary>
    protected override void Run()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        using (RequestSocket client = new RequestSocket())
        {
            client.Connect("tcp://localhost:5559");

            while(true)
            {
                //Debug.Log("Sending GeneralRequest");
                client.SendFrame("getAllData");
                string message = null;
                bool gotMessage = false;
                while (Running && !gotMessage)
                    gotMessage = client.TryReceiveFrameString(out message); // this returns true if it's successful
                // if (gotMessage) Debug.Log("Received " + message);
                if(gotMessage)
                    trueMessage = message;
            }
        }
    }

    public string getTeste()
    {
        return trueMessage;
    }

    public Vector3 getGyro()
    {
        if(trueMessage == null)
            return new Vector3(-99, -99, -99);
        // the data comes in 3 lines (gyro, accel and compass)
        string gyroDataAsString = trueMessage.Split('\n')[0];
        // each value in each line is separeted by a comma (ex.: 0.5, 0.6, 0.7)
        string[] gyroDataArray = gyroDataAsString.Split(',');

        // parsing the data from gyroDataArray
        // ex.:
        // gyroDataArray: {"0.5", "0.6", "0,7"} to {0.5, 0.6, 0,7}
        float[] gyroData = new float[3];
        for(int i = 0; i < 3; i++)
        {
            gyroDataArray[i] = gyroDataArray[i].Replace('.', ',');
            gyroData[i] = float.Parse(gyroDataArray[i]);
        }
        // return as Vector3
        return new Vector3(gyroData[0], gyroData[1], gyroData[2]);
    }
}