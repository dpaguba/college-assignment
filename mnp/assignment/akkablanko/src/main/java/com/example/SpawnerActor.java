package com.example;

import akka.actor.typed.ActorRef;
import akka.actor.typed.javadsl.TimerScheduler;
import akka.actor.typed.Behavior;
import akka.actor.typed.javadsl.AbstractBehavior;
import akka.actor.typed.javadsl.ActorContext;
import akka.actor.typed.javadsl.Behaviors;
import akka.actor.typed.javadsl.Receive;

import java.time.Duration;
import java.util.Random;


public class SpawnerActor extends AbstractBehavior<SpawnerActor.Message> {

    private final TimerScheduler<SpawnerActor.Message> timers;
    private final Random random;
    private final long minTime;
    private final long maxTime;

    public interface Message {}


    public record CreateSingerMessage() implements Message {

    }

    public static Behavior<Message> create(ActorRef<QueueManagerActor.Message> queueManager) {
        return Behaviors.setup(context -> Behaviors.withTimers(timers -> new SpawnerActor(context, timers, queueManager)));
    }

    private SpawnerActor(
            ActorContext<Message> context,
            TimerScheduler<SpawnerActor.Message> timers,
            ActorRef<QueueManagerActor.Message> queueManager
    ) {
        super(context);
        this.timers = timers;
        this.random = new Random();

        this.minTime = 2;
        this.maxTime = 12;

        createRandomDuration(this.minTime, this.maxTime);
    }

    @Override
    public Receive<Message> createReceive() {
        return newReceiveBuilder()
                .onMessage(CreateSingerMessage.class, this::onCreateSingerMessage)
                .build();
    }

    private Behavior<Message> onCreateSingerMessage(CreateSingerMessage msg) {
        this.getContext().spawn(KaraokeSingerActor.create(), "singer");

        createRandomDuration(this.minTime, this.maxTime);
        return this;
    }

    private void createRandomDuration(long minimum, long maximum){
        long interval = this.random.nextInt((int) ((maximum - minimum) + 1)) + minimum;
        Message tempMessage = new CreateSingerMessage();
        Duration durationTime = Duration.ofSeconds(interval);
        this.timers.startSingleTimer(tempMessage, durationTime);
    }
}
# Modified 2025-08-11 10:24:30