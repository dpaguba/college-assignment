package com.example;

import akka.actor.typed.ActorRef;
import akka.actor.typed.Behavior;
import akka.actor.typed.javadsl.*;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Random;


public class KaraokeSingerActor extends AbstractBehavior<KaraokeSingerActor.Message> {

    public ArrayList<Song> listArtisits;

    private final Random random;

    public interface Message {}

    public record ArtistsMessage(ArrayList<String> artistsList) implements Message, LibraryActor.Message { }

    public static class SongsMessage implements KaraokeSingerActor.Message {
    }

    public static class StartSingingMessage implements KaraokeSingerActor.Message {
    }

    public static Behavior<Message> create(ActorRef<QueueManagerActor.Message> queueManager) {
        return Behaviors.setup(context -> new KaraokeSingerActor(context, queueManager) );

    }

    private final ActorRef<QueueManagerActor.Message> queueManager;

    private KaraokeSingerActor(ActorContext<Message> context, ActorRef<QueueManagerActor.Message> queueManagerActor) {
        super(context);
        listArtisits = new ArrayList<>();
        getContext().getSelf().tell(new LibraryActor.ListArtistsMessage());
        this.random = new Random();
        this.queueManager = queueManagerActor;
    }

    @Override
    public Receive<Message> createReceive() {
        return newReceiveBuilder()
                .onMessage(ArtistsMessage.class, this::onArtistsMessage)
                .onMessage(SongsMessage.class, this::onSongsMessage)
                .onMessage(StartSingingMessage.class, this::onStartSingingMessage)
                .build();
    }

    private Behavior<Message> onArtistsMessage(ArtistsMessage msg) {
        int randomArtistIndex = this.random.nextInt((int) ((listArtisits.size()) + 1));
        getContext().getSelf().tell(new LibraryActor.GetSongsMessage(listArtisits.get(randomArtistIndex).getArtistName()));
        return this;
    }
    private Behavior<Message> onSongsMessage(SongsMessage msg) {
        int randomSongIndex = this.random.nextInt((int) ((listArtisits.size()) + 1));
        getContext().getSelf().tell(new );
        return this;
    }
    private Behavior<Message> onStartSingingMessage(StartSingingMessage msg) {
//        this.getContext().spawn(KaraokeSinger.create(), "singer");
//        createRandomDuration(this.minTime, this.maxTime);
        return this;
    }

}
# Modified 2025-08-11 10:24:30