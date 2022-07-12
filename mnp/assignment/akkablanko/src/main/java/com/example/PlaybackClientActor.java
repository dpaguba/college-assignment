package com.example;

import akka.actor.typed.ActorRef;
import akka.actor.typed.Behavior;
import akka.actor.typed.javadsl.*;

import java.time.Duration;


public class PlaybackClientActor extends AbstractBehavior<PlaybackClientActor.Message> {

    public interface Message {}

    public record Init(ActorRef<QueueManagerActor.Message> queueManagerActor) implements Message {}

    public record PlayMessage(String artist, String title, int duration) implements Message {
        public String getTitle() {
            return title;
        }

        public String getArtist() {
            return artist;
        }

        public int getDuration() {
            return duration;
        }
    }


    public static Behavior<Message> create() {
        return Behaviors.setup(context -> Behaviors.withTimers(timers -> new PlaybackClientActor(context, timers)));
    }

    private final TimerScheduler<PlaybackClientActor.Message> timers;

    private PlaybackClientActor(ActorContext<Message> context, TimerScheduler<PlaybackClientActor.Message> timers) {
        super(context);
        this.timers = timers;
        Message msg = new PlayMessage("", "song", 10);
        this.timers.startSingleTimer(msg, msg, Duration.ofSeconds(10));
    }

    @Override
    public Receive<Message> createReceive() {
        return newReceiveBuilder()
                .onMessage(PlayMessage.class, this::onPlayMessage)
                .build();
    }

    private Behavior<Message> onPlayMessage(PlayMessage msg) {

        getContext().getLog().info("Done");

        getContext().getSelf().tell(new QueueManagerActor.ReadyMessage(this.getContext().getSelf()));

        return this;
    }
}

# Modified 2025-08-11 10:24:30