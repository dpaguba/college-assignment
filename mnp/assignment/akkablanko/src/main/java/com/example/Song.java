package com.example;

public class Song {

    private String artistName;
    private String title;
    private int duration;

    public Song(String name, String title, int duration){
        this.artistName = name;
        this.title = title;
        this.duration = duration;
    }

    public String getArtistName() {
        return artistName;
    }
    public String getTitle() {
        return title;
    }
    public int getDuration() {
        return duration;
    }
}

# Modified 2025-08-11 10:24:30