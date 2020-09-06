package com.subhamoy.gymstudentapp.bean;

public class Profile {
    private String id;
    private String name;
    private String age;
    private String phone;
    private String membershipValidity;
    private String allotedtime;

    public Profile() {
    }

    public Profile(String id, String name, String age, String phone, String membershipValidity, String allotedtime) {
        this.id = id;
        this.name = name;
        this.age = age;
        this.phone = phone;
        this.membershipValidity = membershipValidity;
        this.allotedtime = allotedtime;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getAge() {
        return age;
    }

    public void setAge(String age) {
        this.age = age;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getMembershipValidity() {
        return membershipValidity;
    }

    public void setMembershipValidity(String membershipValidity) {
        this.membershipValidity = membershipValidity;
    }

    public String getAllotedtime() {
        return allotedtime;
    }

    public void setAllotedtime(String allotedtime) {
        this.allotedtime = allotedtime;
    }

    @Override
    public String toString() {
        return "Profile{" +
                "id='" + id + '\'' +
                ", name='" + name + '\'' +
                ", age='" + age + '\'' +
                ", phone='" + phone + '\'' +
                ", membershipValidity='" + membershipValidity + '\'' +
                ", allotedtime='" + allotedtime + '\'' +
                '}';
    }
}
