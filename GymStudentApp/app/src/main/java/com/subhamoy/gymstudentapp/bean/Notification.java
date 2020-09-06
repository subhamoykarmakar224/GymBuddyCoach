package com.subhamoy.gymstudentapp.bean;

public class Notification {
    String studentId;
    String gymId;
    String dateTime;
    String level;
    String msg;

    public Notification() {    }


    public Notification(String studentId, String gymId, String dateTime, String level, String msg) {
        this.studentId = studentId;
        this.gymId = gymId;
        this.dateTime = dateTime;
        this.level = level;
        this.msg = msg;
    }

    public String getStudentId() {
        return studentId;
    }

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public String getGymId() {
        return gymId;
    }

    public void setGymId(String gymId) {
        this.gymId = gymId;
    }

    public String getDateTime() {
        return dateTime;
    }

    public void setDateTime(String dateTime) {
        this.dateTime = dateTime;
    }

    public String getLevel() {
        return level;
    }

    public void setLevel(String level) {
        this.level = level;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }
}
