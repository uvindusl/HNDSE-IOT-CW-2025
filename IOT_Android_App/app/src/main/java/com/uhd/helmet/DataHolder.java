package com.uhd.helmet;

public class DataHolder {
    String Helmet_ID;
    String User_ID;
    String Activated_Day;

    public DataHolder(String helmet_ID, String user_ID, String activated_Day) {
        Helmet_ID = helmet_ID;
        User_ID = user_ID;
        Activated_Day = activated_Day;
    }

    public String getHelmet_ID() {
        return Helmet_ID;
    }

    public void setHelmet_ID(String helmet_ID) {
        Helmet_ID = helmet_ID;
    }

    public String getUser_ID() {
        return User_ID;
    }

    public void setUser_ID(String user_ID) {
        User_ID = user_ID;
    }

    public String getActivated_Day() {
        return Activated_Day;
    }

    public void setActivated_Day(String activated_Day) {
        Activated_Day = activated_Day;
    }
}
