package com.example;

import akka.actor.typed.ActorRef;
import akka.actor.typed.Behavior;
import akka.actor.typed.javadsl.*;

import java.util.LinkedList;
import java.util.Queue;


public class QueueManagerActor extends AbstractBehavior<QueueManagerActor.Message> {

    private final Queue<Song> playlist;

    public interface Message {
    }

    public record Init(ActorRef<PlaybackClientActor.Message> playbackClientActor) implements Message {}

    public record ReadyMessage (ActorRef<PlaybackClientActor.Message> replyTo) implements Message, PlaybackClientActor.Message { }

    public static class AddMessage implements QueueManagerActor.Message {
        public String songName;
        public int duration;
        public String artist;
    }
//
//    public record CreateMessage(ActorRef<AkkaMainSystem.Create> someReference) implements QueueManagerActor.Message {
//    }

    public static Behavior<Message> create() {
        return Behaviors.setup(QueueManagerActor::new);
    }

    private QueueManagerActor(ActorContext<Message> context) {
        super(context);
        this.playlist = new LinkedList<>();
    }

    @Override
    public Receive<QueueManagerActor.Message> createReceive() {
        return newReceiveBuilder()
                .onMessage(ReadyMessage.class, this::onReadyMessage)
                .onMessage(AddMessage.class, this::onAddMessage)
                .build();
    }

    private Behavior<Message> onReadyMessage(ReadyMessage msg) {
        if (!this.playlist.isEmpty()) {
            Song firstSong = playlist.poll();
            msg.replyTo.tell(new PlaybackClientActor.PlayMessage(
                    firstSong.getArtistName(),
                    firstSong.getTitle(),
                    firstSong.getDuration()
            ));
        }
        return this;
    }

    private Behavior<Message> onAddMessage(AddMessage msg) {
        if (!this.playlist.isEmpty()) {
//            this.playlist.add(msg.songName);
        } else {
//            getContext().getSelf().tell(new PlaybackClientActor.SongMessage(msg.songName));
        }
        getContext().getLog().info("");
        return this;
    }
}
# Modified 2025-08-11 10:24:30