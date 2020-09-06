package com.subhamoy.gymstudentapp.bean;



public class Attendence {
    private String date;
    private String state; // 0 or 1

    public Attendence() {
    }

    public Attendence(String date, String state) {
        this.date = date;
        this.state = state;
    }

    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    @Override
    public String toString() {
        return "Attendence{" +
                "date='" + date + '\'' +
                ", state='" + state + '\'' +
                '}';
    }
}
