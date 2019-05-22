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
        old = null;
        history = new ArrayList();
        _requester = new Requester();
        _requester.Start();
    }

    void Update()
    {
        message = _requester.getTeste();
        text.text = message;
        if(message != old)
        {
            old = message;
            history.Add(message);
        }
        // Debug.Log(_requester.getTeste());
    }

    public void onPress()
    {
        foreach(string msg in history)
        {
            text.text = msg;
            Debug.Log(msg);
        }
    }

    void onDestroy()
    {
        _requester.Stop();
    }
}
