package com.subhamoy.gymstudentapp.bean;

public class NotifMsg {
    private long counter;
    private String message;

    public NotifMsg() { }

    public NotifMsg(long counter, String message) {
        this.counter = counter;
        this.message = message;
    }

    public long getCounter() {
        return counter;
    }

    public void setCounter(long counter) {
        this.counter = counter;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
