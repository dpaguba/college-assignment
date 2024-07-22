package com.example;

import akka.actor.typed.ActorRef;
import akka.actor.typed.Behavior;
import akka.actor.typed.javadsl.*;

import java.util.ArrayList;
import java.util.List;

public class LibraryActor extends AbstractBehavior<LibraryActor.Message> {

    private List<Song> songs;


    public interface Message {
    }

    public static class GetSongsMessage implements Message, KaraokeSingerActor.Message {
        public final String name;

        public GetSongsMessage(String name) {
            this.name = name;
        }
    }

    public static class ListArtistsMessage implements Message, KaraokeSingerActor.Message {
    }


    public record CreateMessage(ActorRef<AkkaMainSystem.Create> someReference) implements Message {
    }

    public static Behavior<Message> create() {
        return Behaviors.setup(context -> new LibraryActor(context));
    }


    private LibraryActor(ActorContext<Message> context) {
        super(context);

        songs = new ArrayList<>();
        songs.add(new Song("Drake", "Forever", 12));
        songs.add(new Song("Drake", "Headlines", 7));
        songs.add(new Song("Drake", "Best I Ever Had", 9));

        songs.add(new Song("Bad Bunny", "Diles", 10));
        songs.add(new Song("Bad Bunny", "Soy Peor", 9));
        songs.add(new Song("Bad Bunny", "I Like It", 18));

        songs.add(new Song("Ed Sheeran", "Thinking Out Loud", 10));
        songs.add(new Song("Ed Sheeran", "Perfect", 9));
        songs.add(new Song("Ed Sheeran", "Photograph", 9));

        songs.add(new Song("Taylor Swift", "Shake it off", 7));
        songs.add(new Song("Taylor Swift", "Love Story", 8));
        songs.add(new Song("Taylor Swift", "Blank Space", 8));
    }


    @Override
    public Receive<Message> createReceive() {
        return newReceiveBuilder()
                .onMessage(GetSongsMessage.class, this::onGetSongsMessage)
                .onMessage(ListArtistsMessage.class, this::onListArtistsMessage)
                .build();
    }



    private Behavior<Message> onListArtistsMessage(ListArtistsMessage msg) {
        ArrayList<String> artistsList = new ArrayList<String>();
        StringBuilder str = new StringBuilder("Artists: ");
        for (int i = 0; i < songs.size(); i++) {
            if (i == songs.size() - 1){
                str.append(songs.get(i).getArtistName()).append(".");
            }else{
                str.append(songs.get(i).getArtistName()).append(", ");
            }
            artistsList.add(songs.get(i).getArtistName());
        }
        this.getContext().getSelf().tell(new KaraokeSingerActor.ArtistsMessage(artistsList));
        this.getContext().getLog().info("{}", str);
        return this;
    }


    private Behavior<Message> onGetSongsMessage(GetSongsMessage msg) {
        ArrayList<String> songsList = new ArrayList<String>();
        StringBuilder str = new StringBuilder("Artist " + msg.name + " wrote songs: ");
        for (int i = 0; i < songs.size(); i++) {
            if (songs.get(i).getArtistName().equals(msg.name)){
                if (i == songs.size() - 1){
                    str.append(songs.get(i).getTitle()).append(".");
                }else{
                    str.append(songs.get(i).getTitle()).append(", ");
                }
            }
            songsList.add(songs.get(i).getTitle());
        }
        this.getContext().getLog().info("{}", str);
        return this;
    }
}
