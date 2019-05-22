using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Threading;


public class Client : MonoBehaviour
{
    public Requester _requester;
    public Text text;
    private string message, old;
    private ArrayList history;
    void Start()
    {
        _requester = new Requester();
        _requester.Start();
    }

    void Update()
    {
        message = _requester.getGyro().ToString();
        text.text = message;
        // Debug.Log(_requester.getGyro());
        // Debug.Log(_requester.getTeste());
    }

    void onDestroy()
    {
        _requester.Stop();
    }
}
